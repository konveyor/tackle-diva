package io.tackle.diva.windup;

import org.jboss.windup.config.AbstractRuleProvider;
import org.jboss.windup.config.loader.RuleLoaderContext;
import org.jboss.windup.config.metadata.RuleMetadata;
import org.jboss.windup.config.phase.MigrationRulesPhase;
import org.ocpsoft.rewrite.config.Configuration;
import org.ocpsoft.rewrite.config.ConfigurationBuilder;

/**
*/
@RuleMetadata(phase = MigrationRulesPhase.class)
public class DivaRuleProvider extends AbstractRuleProvider {

   // @formatter:off
   @Override
   public Configuration getConfiguration(RuleLoaderContext ruleLoaderContext)
   {
       ClassLoader cl = DivaRuleProvider.class.getClassLoader();
       
       
       System.out.println(cl);       
       
       
       return ConfigurationBuilder.begin()
           .addRule()
           .perform(new DivaLauncher());
   }
   // @formatter:on
}
