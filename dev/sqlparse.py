#	Copyright IBM Corporation 2021
#	
#	Licensed under the Apache Public License 2.0, Version 2.0 (the "License");
#	you may not use this file except in compliance with the License.
#	
#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.


from peg import seq, val, before, choice, star, nil, pegop, pegcxt
from peg import match as match0

def option(v):
    return choice(v, nil)

reserved = [
    'as', 'by', 'in', 'on', 'asc', 'all', 'end', 'set', 'from', 'left', 'join', 'full', 'desc',
    'case', 'when', 'then', 'else', 'into', 'where', 'group', 'inner', 'outer', 'order', 'right',
    'union', 'except', 'select', 'update', 'delete', 'insert', 'null', 'having',
    'listagg', 'within', 'current', 'fetch', 'concat', 'nextval', 'for', 'and', 'or', 'is', 'not',
    'like', 'escape', 'partition', 'exists', 'top', 'using',
    ':_where_in', ':_where_and', ':_where_or', ':_in', ':_or', ':_and',
]

# See https://www.ibm.com/support/knowledgecenter/SSEPEK_10.0.0/sqlref/src/tpc/db2z_reservedwords.html

reserved_that_can_be_names =  [
    'as', 'by', 'in', 'on', 'all', 'set', 'from', 'left', 'join', 'full', 'when', 'then', 'else',
    'where', 'group', 'inner', 'outer', 'order', 'right', 'union', 'except', 'select', 'delete', 'insert',
    'listagg', 'within', 'current', 'fetch', 'concat', 'for', 'partition',
]

what_only_follow_names = [
    ')', ',', 'as', 'in', 'on', 'where', 'then', 'else', 'inner'
]

operator_tokens = [
    '||', '<=', '>=', '<>', '!=', '(+)', '=*', '*=',
]

def token0(s):
    k0 = 0
    while k0 < len(s):
        if not s[k0].isspace():
            break
        k0 += 1
    else:
        return ()
    if k0 + 2 <= len(s) and s[k0:k0+2] in operator_tokens:
        return (s[k0+2:], [s[k0:k0+2]])
    if k0 + 3 <= len(s) and s[k0:k0+3] in operator_tokens:
        return (s[k0+3:], [s[k0:k0+3]])
    k = k0 + 1
    if s[k0].isalpha() or s[k0] == '_' or s[k0] == ':' or s[k0] == '?':
        while k < len(s):
            if not s[k].isalnum() and s[k] != '_' and (s[k] != '-' or s[k0] != ':'):
                break
            k += 1
    elif s[k0].isdigit() or s[k0] == '.':
        p = s[k0] == '.'
        while k < len(s):
            if s[k] == '.' and p:
                break
            elif s[k] == '.':
                p = True
            elif not s[k].isdigit():
                break
            k += 1
    elif s[k0] == "'" or s[k0] == '"':
        while k < len(s):
            if s[k] == s[k0]:
                k += 1
                break
            k += 1
    return (s[k:], [s[k0:k]]) if k > k0 else ()

@pegop
def token1(s):
    r = token0(s)
    if r and r[1][0] in reserved_that_can_be_names:
        r2 = token0(r[0])
        if not r2 or r2[1][0] in what_only_follow_names:
            return (r[0], ['"%s"' % r[1][0]])
    if r and r[1][0] in reserved and r[0] and r[0][0] == '.':
        return (r[0], ['"%s"' % r[1][0]])
    return r

token = token1() # caching tokenization

def name(s):
    r = token(s)
    return (r[0], []) if r and r[1][0] not in reserved and (r[1][0][0] == '_' or r[1][0][0].isalpha() or r[1][0][0] == '"') else ()

def literal(s):
    r = token(s)
    if r and r[1][0][0] == "'":
        return (r[0], [])
    if r and r[1][0] == "null":
        return (r[0], [])
    if r and (r[1][0][0].isdigit() or r[1][0][0] == '.' and len(r[1][0]) > 1):
        return (r[0], [])
    return ()

def variable0(s):
    r = token(s)
    if r and r[1][0][0] == ":":
        return (r[0], [])
    if r and r[1][0] == "?":
        return (r[0], [])
    return ()

@pegop
def op(s, v):
    r = token(s)
    return (r[0], []) if r and r[1][0] == v else ()

@pegop
def until(s, *ws):
    while 1:
        r = token(s)
        if not r:
            return ('', []) if None in ws else ()
        if r[1][0] in ws:
            return (s, [])
        s = r[0]

def match(e, r=None):
    if r is None:
        return match0(e, lambda s, v: s + [v.strip()])
    else:
        return match0(e, lambda s, v: r(s, v.strip()))

def split(n):
    if '.' not in n:
        return ('', n)
    else:
        p = n.rindex('.')
        return (n[:p], n[p+1:])

qname = seq(name, star(seq(op('.'), name)), option(seq(op('@'), name)))

paren = seq(op('('), star(seq(until('(', ')'), lambda s : paren(s))), until('(', ')'), op(')'))

# skip until one of strs occurs, ignoring anything inside parenthesis
until_ignoring_paren = lambda *strs: seq(star(seq(until('(', ')', *strs), paren)), until('(', ')', *strs), until(*strs))

comma_sep = lambda e : seq(e, star(seq(op(','), e)))
plus = lambda e : seq(e, star(e))

# [{ s[-1][None] : s[0] }] if len(s) == 2 and seq(qname, option(op('as')), name)(v) == ('', []) else

ascxt = lambda e: match(seq(e, option(seq(option(op('as')), match(name, lambda s,v: [{None:v}])))),
                        lambda s, v :
                        [{ s[-1][None] : s[0] if len(s) == 2 else s[:-1] }] if s and isinstance(s[-1], dict) and None in s[-1] else
                        s)

variable = choice(variable0, seq(op('#'), op('{'), qname, option(seq(op(','), comma_sep(seq(name, op('='), name)))),  op('}')))

func = choice(qname, variable, op('left'), op('right'), op('concat'))

callargs = choice(
    comma_sep(seq(
        option(choice(op('distinct'), op('all'))),
        choice(
            lambda s : colexp(s),
            match(op('*'), lambda s, v: s + [(v,)])))),
    nil)

callexp = choice(
    seq(op('listagg'), op('('), callargs, op(')'), option(seq(op('within'), op('group'), paren))),
    seq(op('cast'), op('('), lambda s: colexp(s), op('as'), until_ignoring_paren(')'), op(')')),
    seq(func, op('('), callargs, op(')'), option(seq(op('over'), paren))))

caseexp = seq(
    op('case'),
    option(lambda s : colexp(s)),
    plus(seq(op('when'), until_ignoring_paren('then'), op('then'), lambda s : colexp(s))),
    option(seq(op('else'), lambda s: colexp(s))),
    op('end'))

colexp0 = choice(
    literal,
    seq(match(variable, lambda s, v: s + [(v,)]),
        option(seq(op('indicator'),
                   variable))),
    seq(op('current'), name),
    callexp,
    caseexp,
    seq(op('('), comma_sep(lambda s : colexp(s)), op(')')),
    lambda s: nestedexp(s),
    match(seq(name, op('.'), op('*')), lambda s, v: s + [(v,)]),
    seq(option(seq(op('nextval'), op('for'))),
        match(qname, lambda s, v: s + [(v,)]),
        option(seq(op('.'), op('nextval')))),
    seq(op('set'), op('('), lambda s : colexp(s), op(')')))

binaryexp = seq(
    colexp0,
    choice(op('+'), op('-'), op('*'), op('/'), op('||'), op('concat')),
    lambda s: colexp(s))

naryexp = choice(
    seq(op('-'), lambda s: colexp(s)),
    binaryexp)

colexp = choice(naryexp, colexp0)

colexp1 = match(ascxt(colexp), lambda s, _:
                [{ split(s[0][0])[1] : s[0]}] if len(s) == 1 and isinstance(s[0], tuple)
                else s)

#colexp1 = match(ascxt(colexp), lambda s, _:
#                [{s[1].keys()[0] : s[0] }] if len(s) > 1
#                else s)

colsexp = choice(comma_sep(colexp1), match(op('*'), lambda s, v: s + [(v,)]))

jointype = seq(
    choice(
        seq(choice(op('left'), op('right'), op('full')), option(op('outer'))),
        op('inner'),
        nil),
    op('join'), option(op('fetch')))

joincond = seq(op('on'), lambda s : condexp(s))

tblexp = choice(
    seq(match(qname),
        option(seq(op('partition'), op('('), name, op(')')))),
    lambda s : nestedexp(s),
    seq(op('('), lambda s : tblsexp(s), op(')')))

frmcxt = lambda e : match(e, lambda s, _ : [{':from' : s}])

tblsexp = frmcxt(seq(
    ascxt(tblexp),
    star(choice(
        seq(op(','), ascxt(tblexp)),
        seq(jointype, ascxt(tblexp), option(joincond))))))

nestedexp = seq(
    op('('), choice(
        match(lambda s: selexp(s), lambda s, v: [s]),
        match(lambda s: valuesexp(s), lambda s, v: [s]),
        lambda s: nestedexp(s)),
    op(')'))

@pegcxt
def unioncxt(e, fix):
    return seq(
        choice(e, seq(op('('), choice(e, fix), op(')'))),
        star(seq(
            choice(
                seq(op('union'), option(op('all'))),
                op('except')),
            match(choice(e, seq(op('('), choice(e, fix), op(')'))), lambda s, v: [s]))),
        option(grpexp),
        option(orderexp))

@pegcxt
def withcxt(e, fix):
    return choice(
        seq(op('with'),
            comma_sep(seq(
                name,
                option(seq(op('('), comma_sep(name), op(')'))),
                op('as'),
                nestedexp)), e),
        e)

colexp2 = choice(seq(qname, op('(+)')), colexp)

condexp = seq(choice(
    seq(op('('),
        lambda s: condexp(s),
        op(')')),
    seq(op('not'),
        lambda s : condexp(s)),
    seq(op('exists'),
        choice(colexp, lambda s: nestedexp(s))),
    seq(colexp2,
        choice(
            seq(choice(
                op('='), op('<'), op('>'), op('<='), op('>='), op('<>'), op('!='), op('*='), op('=*'),
                seq(op('is'), option(op('not')))),
                colexp2),
            seq(option(op('not')), choice(
                seq(op('in'),
                    choice(colexp, lambda s :nestedexp(s))),
                seq(op('like'),
                    colexp,
                    option(seq(op('escape'), colexp))),
                seq(op('between'),
                    colexp, op('and'), colexp))),
            variable)),
    seq(choice(op(':_where_and'), op(':_or'), op(':_and')), op('('), comma_sep(lambda s : condexp(s)), op(')')),
    seq(op(':_in'), op('('), qname, option(op('=')), variable, op(')')),
    seq(op('current'), op('of'),
        choice(colexp, lambda s: nestedexp(s))),
    callexp),
    option(seq(
        choice(op('and'), op('or')),
        lambda s: condexp(s))))

# whrexp = seq(op('where'), until_ignoring_paren(')', 'group', 'order', 'union', None))
whrexp = choice(
    seq(op('where'), condexp),
    seq(choice(
        seq(op(':_where_in'), colexp),
        seq(choice(op(':_where_and'), op(':_where_or')), op('('), option(condexp),
            star(seq(option(op(',')), choice(condexp, variable))), op(')'))),
        option(seq(choice(op('and'), op('or')),
                   condexp))))

havingexp = seq(op('having'), condexp)

grpexp = seq(op('group'), op('by'), comma_sep(colexp))
orderexp = seq(op('order'), op('by'), comma_sep(seq(colexp, option(choice(op('asc'), op('desc'))))))

assignexp = match(seq(choice(match(qname, lambda s,v: s +[(v,)]),
                       seq(op('('), comma_sep(match(qname, lambda s,v: s +[(v,)])), op(')'))),
                      op('='), colexp),
                  lambda s,v: [s])
assignsexp = seq(assignexp, star(seq(op(','), assignexp)))

frmspec = seq(
    tblsexp,
    option(whrexp),
    option(grpexp),
    option(havingexp),
    option(orderexp),
    option(variable),
    option(seq(op('fetch'), op('first'), choice(literal, variable, nil), op('rows'), op('only'))),
    option(seq(op('for'), op('update'),
               choice(op('nowait'),
                      seq(op('wait'), literal),
                      seq(op('with'), op('rs')),
                      seq(op('of'), comma_sep(qname)),
                      nil))),
    option(seq(op('with'), op('ur'))))


selexp = withcxt(unioncxt(seq(match(op('select')), option(op('distinct')), option(seq(op('top'), literal)), colsexp, option(op(',')), option(seq(op('into'), colsexp)), op('from'), frmspec)))
updexp = withcxt(seq(match(op('update')), frmcxt(seq(ascxt(match(qname)), op('set'), assignsexp)), option(whrexp)))
valuesexp = seq(match(op('values')), op('('), comma_sep(match(colexp, lambda s,v: [s])), op(')'))
insexp = withcxt(seq(match(op('insert')), op('into'),
                     frmcxt(seq(ascxt(match(qname)), option(seq(op('('), comma_sep(match(qname, lambda s,v: s +[(v,)])), op(')'))))),
                     choice(valuesexp, selexp)))
delexp = withcxt(seq(match(op('delete')), option(op('from')), frmcxt(ascxt(match(qname))), option(whrexp)))
mergeexp = seq(match(op('merge')), op('into'), frmcxt(seq(ascxt(match(qname)))), op('using'), star(match(token, lambda s,v: [])))

sqlexp = seq(choice(selexp, updexp, insexp, delexp, valuesexp, mergeexp), option(op(';')))

if __name__ == '__main__':
    print(selexp('select a from b t,c where (a = b)'))
    print(selexp('select a from b t,c'))
    print(selexp('SELECT ACCOUNTID, BALANCE, CREATIONDATE, LASTLOGIN, LOGINCOUNT, LOGOUTCOUNT, OPENBALANCE, PROFILE_USERID FROM accountejb WHERE (PROFILE_USERID = ?)'.lower()))
    print(updexp('UPDATE accountejb SET LOGOUTCOUNT = ? WHERE (ACCOUNTID = ?)'.lower()))
    print(selexp('SELECT t1.HOLDINGID, t1.PURCHASEDATE, t1.PURCHASEPRICE, t1.QUANTITY, t1.ACCOUNT_ACCOUNTID, t1.QUOTE_SYMBOL FROM accountejb t0, holdingejb t1 WHERE ((t0.PROFILE_USERID = ?) AND (t0.ACCOUNTID = t1.ACCOUNT_ACCOUNTID))'.lower()))
    print(sqlexp('INSERT INTO holdingejb (HOLDINGID, PURCHASEDATE, PURCHASEPRICE, QUANTITY, ACCOUNT_ACCOUNTID, QUOTE_SYMBOL) VALUES (?, ?, ?, ?, ?, ?)'.lower()))
    print(sqlexp('DELETE FROM orderejb WHERE (ORDERID = ?)'.lower()))
    print(sqlexp('select dept, LISTAGG(name, \',\') WITHIN GROUP (order by saraly desc nulls last, a asc) csv_name from listagg_sample group by dept'.lower()))
    print(sqlexp('select a as x from b t, (select c from d) u'))
    print(sqlexp('select a as x from b t left outer join ( select * from d ) u on t.i = u.i, e w'))
    print(sqlexp('select count(*) from t'))
    print(sqlexp('with t0 as ( select * from u ), t1 as ( select * from w ) select * from t0, t1'))
    print(sqlexp('select * from t inner join v on t.id = v.id'))
    print(sqlexp('select * from t union select * from u'))
    print(sqlexp("select case when true then 'abc' else col end from t"))
    print(sqlexp('select * from t group by x, y'))
    print(sqlexp('select a.*, count(*) over (partition by id) as c from a, b'))
    print(sqlexp('DELETE orderejb WHERE ORDERID = ?'.lower()))
    print(sqlexp("select * from ((select * from t) union (select * from d) order by x)"))
    print(sqlexp('select * from t for update'))
    print(condexp("a like '%' || ? ||'%'"))
    print(sqlexp('select t0.x, t1.y, t2.z, t3.w from a t0, (select * from b t1, c t2) as t3'))
    print(sqlexp('select d, trim(t.b) || trim(t.c) as a from t'))
    print(sqlexp('select t.a, s.a from s, (select * from x union select * from y) as t'))
    print(selexp('select a into b from c'))
    print(selexp('select set (a) into b from c'))
    print(sqlexp('update accountejb set lastLogin=?, logincount=logincount+1 where profile_userid=?'))
    print(sqlexp('update accountejb set balance = balance + ? where accountid = ?'))
    print(ascxt(match(qname))('a as b'))
    print(ascxt(colexp)('a'))
    print(ascxt(colexp)('a b'))
    print(colexp1('a'))
    print(colexp1('a b'))
    print(variable('?1'))
    #print(sqlexp('select a as x from b t left join c u on t.i = u.i, e w'))
    #print(sqlexp('select m from MerchantConfiguration m join fetch m.merchantStore ms where ms.id=? and m.key=?'.lower()))
    #print(sqlexp('select o from oorder o join fetch o.merchant om join fetch o.orderproducts op left join fetch o.delivery od left join fetch od.country left join fetch od.zone left join fetch o.billing ob left join fetch ob.country left join fetch ob.zone left join fetch o.orderattributes oa join fetch o.ordertotal ot left join fetch o.orderhistory oh left join fetch op.downloads opd left join fetch op.orderattributes opa left join fetch op.prices opp where o.id = ? and om.id = ?'.lower()))
    #print(sqlexp('select t1.usr_id as usrid, t1.usr_nm as usrnm from omck0tbx t1, omc51tbx t2 where t1.usr_id = t2.usr_id and t1.dom_cd = #{domcd} and t2.sys_div_cd = #{sysdivcd} and t2.dep_div_cd in and t2.resp_div_cd = #{respdivcd} order by t1.rcrd_dlflg, t1.usr_id'.lower())) 
    #print(sqlexp('insert into omcr3tbx ( dom_cd, ss_cd_y, ss_cd_mt, model_id, model_nm, model_year, master_software_part_number, rmtecmd_acceptability_flg, sw_insert_flg, send_status, rcrd_dlflg, rcrd_rgts, reg_usrid, rcrd_updts, upd_usrid, equipment_info, mdl, sums_flg ) values ( #{domcd}, #{sscdy}, #{sscdmt}, #{modelid}, #{modelnm}, #{modelyear}, ,#{rmtecmdacceptabilityflg}, #{swinsertflg}, #{sendstatus}, #{rcrddlflg}, sysdate, #{regusrid}, sysdate, #{updusrid}, #{equipmentinfo}, #{mdl}, #{sumsflg} )'))
    #print(sqlexp("select t1.usr_id as usrid ,t1.usr_nm as usrnm from omck0tbx t1, omc51tbx t2"))
    #print(sqlexp("select distinct dev_model as devmodel, ss_cd_m as sscdm from omch3tbx where dom_cd = #{domcd} dom_cd in #{domcd} and rcrd_dlflg = '0' order by dev_model asc"))
    #print(sqlexp("merge into omcdgtbx using dual on (omcdgtbx.vin = #{vin}) when matched then update set results_info_div = #{resultsinfodiv}, destination = #{destination}, war_dist_cd = #{wardistcd}, dom_cd = #{domcd}, brand = #{brand}, ss_cd_m = #{sscdm}, mdl_nm = #{mdlnm}, ss_cd_y = #{sscdy}, grade = #{grade}, ss_cd_t = #{sscdt}, prod_week = #{prodweek}, manuf_plane_nm = #{manufplanenm}, frame_no = #{frameno}, ota_imp_status = '1', dom_imp_status = #{domimpstatus}, rcrd_dlflg = #{rcrddlflg}, rcrd_updts = sysdate, upd_usrid = 'omcba016' when not matched then insert ( vin, results_info_div, destination, war_dist_cd, dom_cd, brand, ss_cd_m, mdl_nm, ss_cd_y, grade, ss_cd_t, prod_week, manuf_plane_nm, frame_no, ota_imp_status, dom_imp_status, rcrd_dlflg, rcrd_rgts, reg_usrid, rcrd_updts, upd_usrid ) values ( #{vin}, #{resultsinfodiv}, #{destination}, #{wardistcd}, #{domcd}, #{brand}, #{sscdm}, #{mdlnm}, #{sscdy}, #{grade}, #{sscdt}, #{prodweek}, #{manufplanenm}, #{frameno}, '1', #{domimpstatus}, #{rcrddlflg}, sysdate, 'omcba016', sysdate, 'omcba016' )"))
    #print(sqlexp("update omcf3tbx set vin = #{vin}, rcrd_dlflg = #{rcrddlflg}, rcrd_updts = sysdate, upd_usrid = #{updusrid} "))
    #print(sqlexp("select b3.dom_cd as domcd, b1.dc_no as dcno, b1.sytzu_pattflg as sytzupattflg, b1.dc_title as dctitle from omc40tbx b1 inner join omc45tbx b2 on b1.dc_no = b2.dc_no inner join omcc5tbx b3 on b2.destination = b3.destination left join omcj0tbx b4 on b2.dc_no = b4.dc_no and b2.ota_file_nm = b4.ota_file_nm and b4.rcrd_dlflg = '0' where b1.dc_no = #{dcno} and b2.instructions_to_gp_flg = '0' and b2.sent_server <> '00' and ( case when b2.sent_server = '30' and b4.delivert_type <> '2' then 1 when ( b2.sent_server in ('10', '20') or ( b2.sent_server = '30' and b4.delivert_type = '2' ) ) and not exists ( select 'x' from omcc2tbx b5 where b2.ss_cd_y = b5.ss_cd_y and substr(b2.ss_cd_mt, 1, 3) = b5.ss_cd_m and substr(b2.ss_cd_mt, 4, 3) = b5.ss_cd_t and b5.rcrd_dlflg = '0' ) then 1 else 0 end ) = 1 and b1.rcrd_dlflg = '0' and b2.rcrd_dlflg = '0' and b3.rcrd_dlflg = '0' for update of b1.dc_no,b2.dc_no"))
    #print(sqlexp("insert into omct2tbx ( trans_mng_no , version_no , process_cd , rb_loc_cd , lang_class , dom_cd , req_rgts , req_usrid , up_seq_no , dl_seq_no , trans_file_path , zip_file_path , first_upload_rgts , valid_status , rcrd_dlflg , rcrd_rgts , reg_usrid , rcrd_updts , upd_usrid ) values ( #{transmngno} ,#{versionno} ,#{processcd} ,#{rbloccd} ,#{langclass} ,#{domcd} ,sysdate ,#{userid} ,null ,#{dlseqno} ,null ,#{zipfilepath, jdbctype=varchar} , sysdate null ,null ,'0' ,sysdate ,#{userid} ,sysdate ,#{userid} )"))
    #print(sqlexp("update omcr2tbx set master_software_part_number = #{mastersoftwarepartnumber}, campaign_storage_size = #{campaignstoragesize}, software_storage_size = #{softwarestoragesize}, temporary_log_storage_size = #{temporarylogstoragesize}, send_status = #{sendstatus}, rcrd_updts = sysdate, upd_usrid = #{updusrid} where and software_part_number = #{softwarepartnumber} and model_id = #{modelid} and sw_insert_flg = #{swinsertflg} and rcrd_dlflg = #{rcrddlflg}"))
    #print(sqlexp("with temp as ( select distinct t11.f_e_m_d, t11.prod_pla_tgt, t11.bom_cd_mdl, t11.bom_cd_e_f, t11.bom_cd_typ, t11.ss_cd_y from omc10tbx t10, omc11tbx t11, omc12tbx t12 where t10.popular_nm = #{popularnm} t10.popular_nm_cd = #{popularnmcd} and t10.popular_nm_cd = t11.popular_nm_cd and t10.rcrd_dlflg = '0' and t11.rcrd_dlflg = '0' and t11.f_e_m_d = t12.f_e_m_d and t11.bom_cd_mdl = t12.bom_cd_mdl and t11.bom_cd_e_f = t12.bom_cd_e_f and t11.bom_cd_typ = t12.bom_cd_typ and t11.prod_pla_tgt = t12.prod_pla_tgt and t12.spec_disp_ptn = #{powerunit} and t12.rcrd_dlflg = '0' ) select distinct t78.y_yyyy as value, t78.y_yyyy as label from temp inner join omc78tbx t78 on t78.y_cd = temp.ss_cd_y and t78.rcrd_dlflg = '0' order by t78.y_yyyy desc"))
    #print(sqlexp("with temp as ( select distinct t11.f_e_m_d, t11.prod_pla_tgt, t11.bom_cd_mdl, t11.bom_cd_e_f, t11.bom_cd_typ, t11.ss_cd_y from omc10tbx t10, omc11tbx t11, omc12tbx t12 where t10.popular_nm = #{popularnm} t10.popular_nm_cd = #{popularnmcd} and t10.popular_nm_cd = t11.popular_nm_cd and t10.rcrd_dlflg = '0' and t11.rcrd_dlflg = '0' and t11.f_e_m_d = t12.f_e_m_d and t11.bom_cd_mdl = t12.bom_cd_mdl and t11.bom_cd_e_f = t12.bom_cd_e_f and t11.bom_cd_typ = t12.bom_cd_typ and t11.prod_pla_tgt = t12.prod_pla_tgt and t12.spec_disp_ptn = #{powerunit} and t12.rcrd_dlflg = '0' ) select distinct t78.y_yyyy as value, t78.y_yyyy as label from temp inner join omc78tbx t78 on t78.y_cd = temp.ss_cd_y and t78.rcrd_dlflg = '0' order by t78.y_yyyy desc"))
    #print(sqlexp("select distinct t11.f_e_m_d, t11.prod_pla_tgt, t11.bom_cd_mdl, t11.bom_cd_e_f, t11.bom_cd_typ, t11.ss_cd_y from omc10tbx t10, omc11tbx t11, omc12tbx t12 where t10.popular_nm = #{popularnm} t10.popular_nm_cd = #{popularnmcd} and t10.popular_nm_cd = t11.popular_nm_cd and t10.rcrd_dlflg = '0' and t11.rcrd_dlflg = '0' and t11.f_e_m_d = t12.f_e_m_d and t11.bom_cd_mdl = t12.bom_cd_mdl and t11.bom_cd_e_f = t12.bom_cd_e_f and t11.bom_cd_typ = t12.bom_cd_typ and t11.prod_pla_tgt = t12.prod_pla_tgt and t12.spec_disp_ptn = #{powerunit} and t12.rcrd_dlflg = '0'"))
    #print(selexp("select t1.ss_cd_mt as sscdmt , t2.y_yyyy as sscdy , t1.mdl_nm as mdlnm , t1.grade as grade ,t1.ss_cd_y || t1.ss_cd_mt as sscdymt from omc45tbx t1 inner join omc78tbx t2 on ( t2.y_cd = t1.ss_cd_y and t2.rcrd_dlflg = #{rcrddlflg} ) inner join omcc5tbx t3 on ( t3.rcrd_dlflg = #{rcrddlflg} and t3.dom_cd = #{domcd} and t3.destination = t1.destination ) where t1.rcrd_dlflg = #{rcrddlflg} and substr(t1.ss_cd_mt,1,3) in ( #{sscdmt} ) and t1.sent_server = #{sentserver} group by t1.ss_cd_mt, t2.y_yyyy, t1.mdl_nm, t1.grade, t1.ss_cd_y || t1.ss_cd_mt order by t1.mdl_nm asc , t2.y_yyyy desc , t1.grade asc"))
    #print(colexp("t.a || t.b"))
    #print(sqlexp("select t1.ss_cd_y || t1.ss_cd_mt as ymt from omc45tbx t1 , omcc5tbx t2 where t1.rcrd_dlflg = '0' and t2.dom_cd = #{domcd} and not exists ( select 'x' from omch3tbx t3 where t3.ss_cd_y || t3.ss_cd_m || t3.ss_cd_t = t1.ss_cd_y || t1.ss_cd_mt and t3.rcrd_dlflg = '0' ) and t1.destination = t2.destination and t1.rb_mdl_reg_flg = '1' and t2.rcrd_dlflg = '0' group by t1.ss_cd_y || t1.ss_cd_mt order by t1.ss_cd_y || t1.ss_cd_mt"))
    #print(sqlexp("WITH TEMP AS ( SELECT DISTINCT TP1.DOCUMENT_NO, TP1.SUB_TASK_NO, TP1.PROJECT_STATUS, TT1.LIMIT_RGTS, TT1.RIMIT_DATE, TO_CHAR(TT1.LIMIT_RGTS, 'YYYY/MM/DD') LIMIT_DATE, TO_CHAR(TT1.RIMIT_DATE, 'YYYY/MM/DD') RELEASE_DATE, TO_CHAR(TP1.RCRD_RGTS, 'YYYY/MM/DD') CREATE_DATE, TT1.PROCESS_CD, TP1.RCRD_RGTS, TP1.RCRD_UPDTS FROM RMCP1TBX TP1 INNER JOIN RMCT1TBX TT1 ON TP1.DOCUMENT_NO = TT1.DOCUMENT_NO AND TP1.SUB_TASK_NO = TT1.SUB_TASK_NO AND TP1.DOM_CD = #{domainCd} AND TP1.PROJECT_STATUS = #{status1} AND TT1.PROCESS_CD = #{processCd1} AND TP1.RCRD_DLFLG = '0' AND TT1.RCRD_DLFLG = '0' AND (TT1.AUTH_FLG IS NULL OR TT1.AUTH_FLG = '1' ) ) SELECT T01.DOCUMENT_NO, T01.SUB_TASK_NO, T01.MIDMIL_KIND, T08.DIVISION_NAME MIDMIL_KIND_TYPE, T01.PROJECT_NAME1 PROJECT_NAME, MP1.POPULAR_NM AS MDL_NM, MP1.DEV_YEAR_BEAM AS DEVELOPMENT_YEAR, MP1.DESTINATION as DEST_CD, MP1.GRADE as GRADE_CD, MP1.YMT as YMT_CD, TEMP.PROJECT_STATUS, TEMP.LIMIT_RGTS, TEMP.RIMIT_DATE AS RELESE_RGTS, TEMP.PROCESS_CD, TEMP.RCRD_RGTS AS REGISTERED_DATE, TEMP.RCRD_UPDTS AS LAST_EDITED_DATE FROM TEMP INNER JOIN RMC01TBX T01 ON TEMP.DOCUMENT_NO = T01.DOCUMENT_NO AND TEMP.SUB_TASK_NO = T01.SUB_TASK_NO AND T01.DOM_CD = #{domainCd} AND T01.RCRD_DLFLG = '0' AND T01.MIDMIL_KIND IN ( #{item} ) INNER JOIN DMC08TBX T08 ON T08.DIVISION_GROUP_CD = '034' AND T08.LANG_CD = #{defaultLang} AND T08.DIVISION_CD = T01.MIDMIL_KIND AND T08.RCRD_DLFLG = '0' AND TEMP.PROJECT_STATUS IN ( #{item} )".lower())[1][1])
    #print(sqlexp("WITH TEMP1 AS ( SELECT TP1.DOCUMENT_NO, MAX(TP1.SUB_TASK_NO) SUB_TASK_NO FROM RMCP1TBX TP1 WHERE TP1.DOCUMENT_NO = #{docNo} AND TP1.SUB_TASK_NO < #{subNo} AND TP1.PROJECT_STATUS <> '001' AND TP1.RCRD_DLFLG = '0' GROUP BY TP1.DOCUMENT_NO ), TEMP2 AS ( SELECT P1.DOCUMENT_NO, P1.SUB_TASK_NO, P1.PROJECT_STATUS, MAX(T1.PROCESS_CD) PROCESS_CD FROM TEMP1, RMCP1TBX P1, RMCT1TBX T1 WHERE P1.DOCUMENT_NO = TEMP1.DOCUMENT_NO AND P1.SUB_TASK_NO = TEMP1.SUB_TASK_NO AND P1.DOCUMENT_NO = T1.DOCUMENT_NO AND P1.SUB_TASK_NO = T1.SUB_TASK_NO AND P1.RCRD_DLFLG = '0' AND T1.RCRD_DLFLG = '0' GROUP BY P1.DOCUMENT_NO, P1.SUB_TASK_NO, P1.PROJECT_STATUS ) SELECT DOCUMENT_NO DOC_NO, SUB_TASK_NO SUB_NO, PROJECT_STATUS, PROCESS_CD, CASE WHEN MIN_PROCESS_STATUS = MAX_PROCESS_STATUS THEN MAX_PROCESS_STATUS WHEN (MIN_PROCESS_STATUS = '6009' OR MAX_PROCESS_STATUS = '6009') THEN '6009' ELSE MIN_PROCESS_STATUS END PROCESS_STATUS FROM ( SELECT TEMP2.DOCUMENT_NO, TEMP2.SUB_TASK_NO, TEMP2.PROJECT_STATUS, TEMP2.PROCESS_CD, MIN(T1T.PROCESS_STATUS) MIN_PROCESS_STATUS, MAX(T1T.PROCESS_STATUS) MAX_PROCESS_STATUS FROM TEMP2, RMCT1TBX T1T WHERE T1T.DOCUMENT_NO = TEMP2.DOCUMENT_NO AND T1T.SUB_TASK_NO = TEMP2.SUB_TASK_NO AND T1T.DOCUMENT_NO = TEMP2.DOCUMENT_NO AND T1T.PROCESS_CD = TEMP2.PROCESS_CD AND T1T.RCRD_DLFLG = '0' GROUP BY TEMP2.DOCUMENT_NO, TEMP2.SUB_TASK_NO, TEMP2.PROJECT_STATUS, TEMP2.PROCESS_CD )".lower())[1][1])


    print(sqlexp("SELECT ISSUEDATE, EXPIRYDATE, LASTCHANGED, BROKERID, BROKERSREFERENCE, PAYMENT, WITHPROFITS, EQUITIES, MANAGEDFUND, FUNDNAME, TERM, SUMASSURED, LIFEASSURED, PADDINGDATA, LENGTH(PADDINGDATA) FROM POLICY,ENDOWMENT WHERE ( POLICY.POLICYNUMBER = ENDOWMENT.POLICYNUMBER AND POLICY.CUSTOMERNUMBER = :DB2-CUSTOMERNUM-INT AND POLICY.POLICYNUMBER = :DB2-POLICYNUM-INT )".lower()))
    print(variable(":DB2-ISSUEDATE".lower()))
    print(colsexp(":DB2-ISSUEDATE, :DB2-EXPIRYDATE, :DB2-LASTCHANGED, :DB2-BROKERID-INT INDICATOR :IND-BROKERID, :DB2-BROKERSREF INDICATOR :IND-BROKERSREF, :DB2-PAYMENT-INT INDICATOR :IND-PAYMENT, :DB2-E-WITHPROFITS, :DB2-E-EQUITIES, :DB2-E-MANAGEDFUND, :DB2-E-FUNDNAME, :DB2-E-TERM-SINT, :DB2-E-SUMASSURED-INT, :DB2-E-LIFEASSURED, :DB2-E-PADDINGDATA INDICATOR :IND-E-PADDINGDATA, :DB2-E-PADDING-LEN INDICATOR :IND-E-PADDINGDATAL".lower())) 
    
