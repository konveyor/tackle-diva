package io.tackle.diva.analysis;

import java.util.HashSet;
import java.util.Set;

import com.ibm.wala.shrikeBT.BinaryOpInstruction;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSABinaryOpInstruction;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSANewInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.ssa.SSAReturnInstruction;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.util.intset.IntPair;

import io.tackle.diva.Constants;
import io.tackle.diva.Framework;
import io.tackle.diva.Trace;

public class StringAnalysis {

    public static String calculateReachingString(Framework fw, Trace.Val value) {
        return calculateReachingString(fw, value, new HashSet<>());
    }

    public static String calculateReachingString(Framework fw, Trace.Val value, Set<IntPair> visited) {

        if (value == null || value.isParam()) {
            return "??";
        }

        if (value.isConstant()) {
            if (value.constant() == null)
                return "??";
            return value.constant().toString();
        }

        if (fw.methodsTreatedAsIdentity.contains(value.trace().node().getMethod().getReference())) {
            return calculateReachingString(fw, value.getDef(2), visited); // first param
        }

        SSAInstruction instr = value.instr();

        if (instr instanceof SSABinaryOpInstruction) {
            SSABinaryOpInstruction bin = (SSABinaryOpInstruction) instr;
            if (bin.getOperator() == BinaryOpInstruction.Operator.ADD) {
                return calculateReachingString(fw, value.getDef(bin.getUse(0)), visited)
                        + calculateReachingString(fw, value.getDef(bin.getUse(1)), new HashSet<>());
            }

        } else if (instr instanceof SSAGetInstruction) {
            Trace.Val v = PointerAnalysis.fromInits(fw, value.trace(), (SSAGetInstruction) instr);
            if (v != null) {
                return calculateReachingString(fw, v, visited);
            }

        } else if (instr instanceof SSAPhiInstruction) {
            SSAPhiInstruction phi = (SSAPhiInstruction) instr;
            Trace.Val lhs = value.getDef(phi.getUse(0));
            Trace.Val rhs = value.getDef(phi.getUse(1));

            if (lhs.isConstant()) {
                return calculateReachingString(fw, lhs, visited);
            } else if (rhs.isConstant()) {
                return calculateReachingString(fw, rhs, visited);
            }
            int bbid = lhs.trace().node().getIR().getBasicBlockForInstruction(lhs.instr()).getNumber();
            IntPair key = IntPair.make(value.trace().node().getGraphNodeId(), bbid);
            if (visited.contains(key)) {
                return calculateReachingString(fw, rhs, visited);
            }
            visited.add(key);
            return calculateReachingString(fw, lhs, visited);

        } else if (instr instanceof SSAAbstractInvokeInstruction) {
            MethodReference mref = ((SSAAbstractInvokeInstruction) instr).getDeclaredTarget();
            if (mref.getDeclaringClass().getName() == Constants.LJavaLangStringBuffer
                    || mref.getDeclaringClass().getName() == Constants.LJavaLangStringBuilder) {

                if (mref.getName() == Constants.toString) {
                    Trace.Val lastVal = value.getReceiverUseOrDef(visited);
                    return calculateReachingString(fw, lastVal, visited);
                } else if (mref.getName() == Constants.append) {
                    Trace.Val lastVal = value.getReceiverUseOrDef(visited);
                    return calculateReachingString(fw, lastVal, visited)
                            + calculateReachingString(fw, value.getDef(instr.getUse(1)), new HashSet<>());
                } else if (mref.getName() == Constants.theInit) {
                    if (mref.getNumberOfParameters() == 0) {
                        return "";
                    } else if (mref.getParameterType(0).isPrimitiveType()) {
                        return "";
                    }
                    return calculateReachingString(fw, value.getDef(instr.getUse(1)), visited);
                }
            }

            if (mref.getDeclaringClass().getName() == Constants.LJavaLangString && (mref.getName() == Constants.trim
                    || mref.getName() == Constants.strip || mref.getName() == Constants.toUpperCase
                    || mref.getName() == Constants.toLowerCase || mref.getName() == Constants.replaceAll)) {
                return calculateReachingString(fw, value.getDef(instr.getUse(0)), visited);
            }

            if (!fw.stringDictionary.isEmpty() && instr.getNumberOfUses() == 2
                    && (mref.getDeclaringClass().getName() == Constants.LJavaUtilHashtable
                            || mref.getDeclaringClass().getName() == Constants.LJavaUtilHashMap
                            || mref.getDeclaringClass().getName() == Constants.LJavaUtilProperties)
                    && (mref.getName() == Constants.get || mref.getName() == Constants.getProperty)) {

                String key = calculateReachingString(fw, value.getDef(instr.getUse(1)), visited);
                if (fw.stringDictionary.containsKey(key)) {
                    return fw.stringDictionary.get(key);
                }
            }

        } else if (instr instanceof SSANewInstruction) {
            SSANewInstruction alloc = (SSANewInstruction) instr;
            if (alloc.getConcreteType().getName() == Constants.LJavaLangString) {
                SSAAbstractInvokeInstruction constr = StringAnalysis.getConstructorForNew(value.trace().node().getIR(),
                        alloc);
                if (constr.getNumberOfUses() == 2) {
                    return calculateReachingString(fw, value.trace().getDef(constr.getUse(1)), visited);
                }
            }

        } else if (instr instanceof SSAReturnInstruction) {
            Trace.Val lastVal = value.getReceiverUseOrDef(visited);
            return calculateReachingString(fw, lastVal, visited);
        }

        return "??";
    }

    public static SSAAbstractInvokeInstruction getConstructorForNew(IR ir, SSANewInstruction alloc) {
        for (int i = alloc.iIndex() + 1; i < ir.getInstructions().length; i++) {
            SSAInstruction instr = ir.getInstructions()[i];
            if (instr == null || !(instr instanceof SSAAbstractInvokeInstruction) || instr.getNumberOfUses() == 0
                    || instr.getUse(0) != alloc.getDef())
                continue;
            SSAAbstractInvokeInstruction constr = (SSAAbstractInvokeInstruction) instr;
            if (constr.getDeclaredTarget().getName() != Constants.theInit)
                return null;
            return constr;
        }
        return null;
    }

}
