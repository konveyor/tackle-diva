/*
Copyright IBM Corporation 2021

Licensed under the Apache Public License 2.0, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package io.tackle.diva;

import java.util.function.Function;

public interface Report {

    String ENTRY = "entry";
    String METHODS = "methods";
    String HTTP_PARAM = "http-param";
    String TRANSACTIONS = "transactions";
    String TRANSACTION = "transaction";
    String TXID = "txid";
    String OPID = "opid";
    String STACKTRACE = "stacktrace";
    String METHOD = "method";
    String FILE = "file";
    String POSITION = "position";
    String SQL = "sql";
    String REST_CALL = "rest-call";
    String HTTP_METHOD = "http-method";
    String CLIENT_CLASS = "client-class";
    String URL_PATH = "url-path";
    String DISPATCH = "dispatch";

    void add(Named.Builder builder);

    void add(Report.Builder builder);

    void add(String data);

    void add(Integer data);

    @FunctionalInterface
    public interface Builder {
        void build(Report list);
    }

    public interface Named {
        void putPrimitive(String key, Object value);

        default void put(String key, String value) {
            putPrimitive(key, value);
        }

        default void put(String key, Integer value) {
            putPrimitive(key, value);
        }

        default void put(String key, Boolean value) {
            putPrimitive(key, value);
        }

        void put(String key, Named.Builder builder);

        void put(String key, Report.Builder builder);

        default <T> void put(String key, T data, Function<T, Report.Builder> fun) {
            put(key, fun.apply(data));
        }

        @FunctionalInterface
        interface Builder {
            void build(Named map);
        }
    }
}
