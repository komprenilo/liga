// Imported from https://github.com/ml86/mill-antlr
import mill._
import mill.define._
import mill.scalalib._
import $ivy.`org.antlr:antlr4:4.8`
import org.antlr.v4.tool.{ANTLRMessage, ANTLRToolListener}

import scala.collection.mutable

trait AntlrModule extends JavaModule {
  def antlrGrammarSources: Sources
  def antlrPackage: Option[String] = None
  def antlrGenerateVisitor: Boolean = false
  def antlrGenerateListener: Boolean = false

  def antlrGrammarSourceFiles = T {
    antlrGrammarSources().flatMap { source =>
      if (os.isDir(source.path)) {
        os.walk(source.path)
      } else {
        Seq(source.path)
      }
    }.filter { path =>
      os.isFile(path) && path.ext == "g4"
    }.map(PathRef(_))
  }

  def antlrGenerate = T {
    val antlrToolArgs = mutable.ArrayBuffer.empty[String]

    antlrToolArgs.appendAll(antlrGrammarSourceFiles().map(_.path.toString))
    antlrToolArgs.append("-o")
    antlrToolArgs.append(s"${T.dest}")
    if (antlrPackage.isDefined) {
      antlrToolArgs.append("-package")
      antlrToolArgs.append(antlrPackage.get)
    }
    if (antlrGenerateVisitor) {
      antlrToolArgs.append("-visitor")
    }
    if (antlrGenerateListener) {
      antlrToolArgs.append("-listener")
    }

    val antlrTool = new org.antlr.v4.Tool(antlrToolArgs.toArray)
    antlrTool.processGrammarsOnCommandLine()

    os.walk(T.dest).filter(path => os.isFile(path) && path.ext == "java").map(PathRef(_))
  }

  override def generatedSources = T {
    super.generatedSources() ++ antlrGenerate()
  }
}
