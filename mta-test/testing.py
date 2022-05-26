from __future__ import print_function

import os, glob, sys, yaml, re, time
from datetime import timedelta

def get_opts(argv=['']):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('input', nargs='?', default='divaapps.txt', help='github urls')
    p.add_argument('-o', '--overwrite', action='store_true')
    return p.parse_args(argv)

def run(opts):
    for url in open(opts.input):
        url = url.strip()
        if not url:
            continue
        name = url[url.rindex('/')+1:]
        if name.endswith('.git'):
            name = name[:-4]
        if os.path.exists(name + '.report') and not opts.overwrite:
            continue
            
        if not os.path.exists(name):
            os.system('git clone {} >&2'.format(url))
        logfile = os.environ['HOME'] + '/.mta/log/mta.log'

        print(name, file=sys.stderr)
        print(url, file=sys.stderr)
        print(logfile, file=sys.stderr)
        print('cp {} {}.report/mta.log >&2'.format(logfile, name), file=sys.stderr)
        
        os.system('rm {} >&2'.format(logfile))

        start = time.time()

        os.system('MAX_MEMORY=16g bash {}/bin/mta-cli --target java-ee --enableTransactionAnalysis --batchMode --overwrite --input {} --sourceMode >&2'.format(os.environ['MTA_HOME'], name))
        os.system('cp {} {}.report/mta.log >&2'.format(logfile, name))

        elapsed = (time.time() - start)

        # running time, success or failure

        has_report = bool(glob.glob(name + '.report/index.html'))
        has_diva_report = bool(glob.glob(name + '.report/reports/diva*.html'))

        diva_exc = False

        wala_ir_total, wala_ir_fail, tr_analysis_total, tr_analysis_fail, diva_elapsed = 0, 0, 0, 0, 0

        for log in open(logfile):
            if 'Diva runs in' in log:
                source_mdoe = 'source' in log
                diva_exc = True
            if 'Diva: DONE' in log or 'Diva: Found no entry methods for analysis' in log:
                diva_exc = False
            wala_ir = re.search(r'wala IR: (.*) classes \((.*) failed\)', log)
            if wala_ir:
                wala_ir_total =  int(wala_ir.group(1))
                wala_ir_fail =  int(wala_ir.group(2))
            tr_analysis = re.search(r'Diva: transaction analysis: (.*)/(.*) \((.*) failures\)', log)
            if tr_analysis:
                tr_analysis_total = int(tr_analysis.group(2))
                tr_analysis_fail = int(tr_analysis.group(3))

        if os.path.exists(name + '.report/stats/timing.txt'):
            for stat in open(name + '.report/stats/timing.txt'):
                diva_stat = re.search(r'(.*), DivaRuleProvider', stat)
                if diva_stat:
                    diva_elapsed = float(diva_stat.group(1))

        print(yaml.dump([{
            'name' : name,
            'giturl' : url,
            'has_report' : has_report,
            'has_diva_report' : has_diva_report,
            'diva_exc': diva_exc,
            'wala_ir_total': wala_ir_total,
            'wala_ir_fail': wala_ir_fail,
            'tr_analysis_total': tr_analysis_total,
            'tr_analysis_fail': tr_analysis_fail,
            'elapsed': str(timedelta(seconds=elapsed)),
            'diva_elapsed': str(timedelta(seconds=diva_elapsed))
        }]), file=sys.stdout)
        sys.stdout.flush()

if __name__ == '__main__':

    if 'JAVA_HOME' not in os.environ or 'MTA_HOME' not in os.environ:
        print('set JAVA_HOME and MTA_HOME appropriately', file=sys.stderr)
        exit(0)

    print('JAVA_HOME = %s' % os.environ['JAVA_HOME'], file=sys.stderr)
    print('MTA_HOME = %s' % os.environ['MTA_HOME'], file=sys.stderr)

    opts = get_opts(sys.argv[1:])
    run(opts)


    

