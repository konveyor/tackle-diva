package io.tackle.diva.analysis;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.types.MethodReference;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.Framework;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;

public class SpringBootAnalysis {

    public static Context.CallSiteVisitor getTransactionAnalysis(Framework fw, Context context) {
        return context.new CallSiteVisitor() {

            @SuppressWarnings("unused")
            @Override
            public void visitCallSite(Trace trace) {

                CGNode node = trace.node();
                CallSiteReference site = trace.site();
                MethodReference ref = site.getDeclaredTarget();
                int pos = -1;
                if (ref.getDeclaringClass().getName() == Constants.LSpringJdbcTemplate) {
                    if (ref.getName() == Constants.queryForObject || ref.getName() == Constants.update) {
                        pos = 0;
                    }
                }
                if (pos >= 0) {
                    if (!fw.txStarted()) {
                        fw.reportSqlStatement(trace, "BEGIN");
                    }
                    JDBCAnalysis.analyzeSqlStatement(fw, trace, site, pos);
                }

            }

            @Override
            public void visitExit(Trace trace) {
                if (!fw.txStarted())
                    return;
                IClass c = trace.node().getMethod().getDeclaringClass();
                if (!Util.any(Util.getAnnotations(c), a -> a.getType().getName() == Constants.LSpringTransactional))
                    return;
                if (trace.parent() == null || !Util.any(trace.parent(), t -> {
                    IClass d = t.node().getMethod().getDeclaringClass();
                    return Util.any(Util.getAnnotations(d),
                            a -> a.getType().getName() == Constants.LSpringTransactional);
                })) {
                    fw.reportSqlStatement(trace, "COMMIT");
                    fw.reportTxBoundary();
                }
            }
        };
    }

}
