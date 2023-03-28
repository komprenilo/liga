import mill._
import mill.scalalib._
import mill.scalalib.publish._
import mill.scalalib.scalafmt._
import mill.modules.Assembly
import mill.modules.Assembly.Rule.ExcludePattern
import $file.antlr

class LigaModule(majorVersion: String) extends CrossScalaModule with PublishModule with ScalafmtModule with antlr.AntlrModule {
  override def crossScalaVersion: String = majorVersion match {
    case "2.12" => "2.12.16"
    case "2.13" => "2.13.8"
    case _ => ???
  }

  def sparkVersion: String = {
    sys.env.get("SPARK_VERSION") match {
      case Some(v) => v
      case None => "3.2.1"
    }
  }

  override def publishVersion = "0.2.3-SNAPSHOT"

  override def artifactId = s"liga-spark_${majorVersion}"

  override def pomSettings = PomSettings(
    description = "Liga",
    organization = "net.xmacs.liga",
    licenses = Seq(License.Common.Apache2),
    url = "https://github.com/komprenilo/liga",
    versionControl = VersionControl.github("komprenilo", "liga"),
    developers = Seq(
      Developer("da-tubi", "Darcy Shen", "https://github.com/da-tubi")
    )
  )

  def scalacOptions = majorVersion match {
    case "2.12" =>
      super.scalacOptions()
    case "2.13" =>
      Seq("-Ymacro-annotations", "-language:postfixOps")
    case _ => ???
  }


  override def compileIvyDeps = majorVersion match {
    case "2.12" => Agg(
      ivy"org.apache.spark::spark-sql:${sparkVersion}",
      ivy"org.antlr:antlr4-runtime:4.8",
      ivy"org.apache.httpcomponents:httpclient:4.5.14",
      ivy"org.scalamacros:::paradise:2.1.1",
      ivy"com.thoughtworks.enableIf::enableif:1.1.8",
    )
    case "2.13" => Agg(
      ivy"org.apache.spark::spark-sql:${sparkVersion}",
      ivy"org.antlr:antlr4-runtime:4.8",
      ivy"org.apache.httpcomponents:httpclient:4.5.14",
      ivy"com.thoughtworks.enableIf::enableif:1.1.8",
    )
    case _ => ???
  }
  

  def scalacPluginIvyDeps = majorVersion match {
    case "2.12" =>
      super.scalacPluginIvyDeps() ++ Agg(
        ivy"org.scalamacros:::paradise:2.1.1"
      )
    case "2.13" =>
      super.scalacPluginIvyDeps()
    case _ => ???
  }

  override def antlrGenerateVisitor: Boolean = true

  override def antlrPackage: Option[String] = Some("net.xmacs.liga.spark.parser")

  override def antlrGrammarSources = T.sources {
    Seq(millSourcePath / "resources" / "antlr4").map(PathRef(_))
  }

  def assemblyRules = Assembly.defaultRules ++ Seq(ExcludePattern("scala/.*"))

  object test extends Tests with TestModule.ScalaTest {
    override def ivyDeps = Agg(
      ivy"org.apache.spark::spark-sql:${sparkVersion}",
      ivy"org.antlr:antlr4-runtime:4.8",
      ivy"org.scalatest::scalatest:3.2.0",
      ivy"org.apache.httpcomponents:httpclient:4.5.14",
      ivy"ch.qos.logback:logback-classic:1.2.3",
    )

    override def forkEnv = Map("LOG_LEVEL" -> "ERROR")
  }
}

object liga extends mill.Cross[LigaModule]("2.12", "2.13")


class ImageModule(majorVersion: String) extends CrossScalaModule with PublishModule with ScalafmtModule {
  override def crossScalaVersion: String = majorVersion match {
    case "2.12" => "2.12.13"
    case "2.13" => "2.13.7"
    case _ => ???
  }

  override def publishVersion = "0.2.0"

  override def artifactId = s"liga-image_${majorVersion}"

  override def pomSettings = PomSettings(
    description = "Image related UDT/UDF on Apache Spark",
    organization = "net.xmacs.liga",
    licenses = Seq(License.Common.Apache2),
    url = "https://github.com/komprenilo/liga-vision",
    versionControl = VersionControl.github("komprenilo", "liga-vision"),
    developers = Seq(
      Developer("da-tubi", "Darcy Shen", "https://github.com/da-tubi")
    )
  )

  override def ivyDeps = Agg(
    ivy"net.xmacs.liga::liga-spark:0.2.2",
  )

  override def compileIvyDeps = Agg(
    ivy"org.apache.spark::spark-sql:3.2.1",
  )

  def assemblyRules = Assembly.defaultRules ++ Seq(ExcludePattern("scala/.*"))

  object test extends Tests with TestModule.ScalaTest {
    override def ivyDeps = Agg(
      ivy"org.apache.spark::spark-sql:3.2.1",
      ivy"org.scalatest::scalatest:3.0.8",
      ivy"ch.qos.logback:logback-classic:1.2.3",
    )

    override def forkEnv = Map("LOG_LEVEL" -> "ERROR")
  }
}

object image extends mill.Cross[ImageModule]("2.12", "2.13")
