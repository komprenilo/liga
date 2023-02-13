ThisBuild / organization := "net.xmacs.liga"
ThisBuild / organizationHomepage := Some(url("https://github.com/liga-ai"))

ThisBuild / scmInfo := Some(
  ScmInfo(
    url("https://github.com/liga-ai/liga"),
    "scm:git@github.com:liga-ai/liga.git"
  )
)

ThisBuild / developers := List(
  Developer(
    id = "da-tubi",
    name = "Darcy Shen",
    email = "da@tubi.tv",
    url = url("https://github.com/da-tubi")
  )
)

ThisBuild / description := "Liga: the ML-Enhanced Spark SQL"
ThisBuild / licenses := List(
  "Apache 2" -> new URL("http://www.apache.org/licenses/LICENSE-2.0.txt")
)
ThisBuild / homepage := Some(url("https://github.com/liga-ai/liga"))

// Remove all additional repository other than Maven Central from POM
ThisBuild / pomIncludeRepository := { _ => false }
ThisBuild / publishMavenStyle := true

publishTo := sonatypePublishToBundle.value
sonatypeCredentialHost := "s01.oss.sonatype.org"
sonatypeRepository := "https://s01.oss.sonatype.org/service/local"
sonatypeProfileName := "net.xmacs.liga"
