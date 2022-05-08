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

FROM gradle:jdk11 as build

WORKDIR /home/gradle
COPY core diva

WORKDIR /home/gradle/diva
RUN gradle ziptask
RUN jar xvf build/distributions/diva-all.zip

FROM eclipse-temurin:11-jre-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --update --no-cache python3 graphviz ttf-freefont git bash && \
    ln -sf python3 /usr/bin/python && \
    python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip pyyaml 

RUN mkdir -p /diva-distribution/lib
COPY distrib/ /diva-distribution/
COPY --from=build /home/gradle/diva/bin/*.jar /diva-distribution/bin/
COPY --from=build /home/gradle/diva/lib/*.jar /diva-distribution/lib/

WORKDIR /diva-distribution/bin
ENTRYPOINT [ "bash" ]
CMD [ "./diva", "/app"]
