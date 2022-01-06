package io.tackle.diva.windup;

import java.nio.file.Paths;

import javax.inject.Inject;

import org.jboss.arquillian.container.test.api.Deployment;
import org.jboss.arquillian.junit.Arquillian;
import org.jboss.forge.arquillian.AddonDependencies;
import org.jboss.forge.arquillian.archive.AddonArchive;
import org.jboss.shrinkwrap.api.ShrinkWrap;
import org.jboss.windup.exec.WindupProcessor;
import org.jboss.windup.exec.configuration.WindupConfiguration;
import org.jboss.windup.graph.GraphContext;
import org.jboss.windup.graph.GraphContextFactory;
import org.jboss.windup.rules.apps.diva.EnableTransactionAnalysisOption;
import org.jboss.windup.rules.apps.java.config.SourceModeOption;
import org.jboss.windup.rules.apps.java.model.WindupJavaConfigurationModel;
import org.jboss.windup.rules.apps.java.service.WindupJavaConfigurationService;
import org.junit.Test;
import org.junit.runner.RunWith;

@RunWith(Arquillian.class)
public class DaytraderQuarkusTest {

    @Deployment
    @AddonDependencies
    public static AddonArchive getDeployment() {
        final AddonArchive archive = ShrinkWrap.create(AddonArchive.class).addBeansXML();
        return archive;
    }

    @Inject
    private WindupProcessor processor;

    @Inject
    private GraphContextFactory contextFactory;

    @Test
    public void testDayTrader() throws Exception {
        try (GraphContext context = contextFactory.create(true)) {
            WindupJavaConfigurationModel javaCfg = WindupJavaConfigurationService.getJavaConfigurationModel(context);
            javaCfg.setSourceMode(true);

            WindupConfiguration wc = new WindupConfiguration();
            wc.setGraphContext(context);
            String app = "../../daytrader-quarkus/";

            wc.addInputPath(Paths.get(app));
            wc.setOutputDirectory(Paths.get("target/WindupReport/daytrader-quarkus"));
            wc.setOptionValue(SourceModeOption.NAME, true);
            wc.setOptionValue(EnableTransactionAnalysisOption.NAME, true);

            processor.execute(wc);
        }
    }

}
