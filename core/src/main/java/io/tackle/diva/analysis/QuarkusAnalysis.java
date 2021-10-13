package io.tackle.diva.analysis;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeCT.AnnotationsReader.ConstantElementValue;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.types.annotations.Annotation;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.Framework;
import io.tackle.diva.Report;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;

public class QuarkusAnalysis {

    public static List<IMethod> getEntries(IClassHierarchy cha) throws IOException {
        List<IMethod> entries = new ArrayList<>();

        for (IClass c : cha) {
            if (c.isInterface())
                continue;
            if (Util.any(Util.getAnnotations(c), a -> a.getType().getName() == Constants.LJavaxWsRsPath)) {
                for (IMethod m : c.getDeclaredMethods()) {
                    if (Util.any(Util.getAnnotations(m), a -> a.getType().getName() == Constants.LJavaxWsRsPath)) {
                        entries.add(m);
                    }
                }
            }
        }
        return entries;

    }

    public static Context.CallSiteVisitor getTransactionAnalysis(Framework fw, Context context) {
        return context.new CallSiteVisitor() {

            @SuppressWarnings("unused")
            @Override
            public void visitCallSite(Trace trace) {

                CGNode node = trace.node();
                CallSiteReference site = trace.site();
                MethodReference ref = site.getDeclaredTarget();
                TypeReference tref = ref.getDeclaringClass();
                IClass c = fw.classHierarchy().lookupClass(tref);

                if (c != null && Util.any(Util.getAnnotations(c),
                        a -> a.getType().getName() == Constants.LMicroprofileReigsterRestClient)) {
                    IMethod m = c.getMethod(ref.getSelector());

                    String method = null;
                    String path = null;

                    for (Annotation a : Util.getAnnotations(m)) {
                        if (a.getType().getName() == Constants.LJavaxWsRsGET) {
                            method = "GET";
                        } else if (a.getType().getName() == Constants.LJavaxWsRsPOST) {
                            method = "POST";
                        } else if (a.getType().getName() == Constants.LJavaxWsRsPATCH) {
                            method = "PATCH";
                        } else if (a.getType().getName() == Constants.LJavaxWsRsDELETE) {
                            method = "DELETE";
                        }
                        if (a.getType().getName() == Constants.LJavaxWsRsPath) {
                            path = ((ConstantElementValue) a.getNamedArguments().get("value")).val.toString();
                        }
                    }
                    if (method != null) {
                        String httpMethod = method;
                        String httpPath = path;
                        fw.reportOperation(trace, (Report.Named named) -> {
                            named.put("rest-call", (Report.Named map) -> {
                                map.put("http-method", httpMethod);
                                map.put("url-path", httpPath);
                                map.put("client-class", c.getName().toString());
                            });
                        });
                        // Util.LOGGER.info("method = " + method + ", path = " + path + ", client = " +
                        // c + ", module = "
                        // + c.getClassLoader().getReference());
                    }
                }
            }
        };
    }

}
