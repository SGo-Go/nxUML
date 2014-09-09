<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <xsl:template name="show-html-default">
    <html lang="en">
      <head>
	<link rel="shortcut icon" type="image/x-icon" href="css/icons/favicon.ico" />
	<meta charset="utf-8"/>
	<meta name="viewport" content="width=device-width,initial-scale=1"/>

	<link rel="stylesheet" href="css/style.css"/>
	<title>MapCtrl documentation [Class <xsl:call-template name="show-name"/>]</title>
	<!--[if lt IE 9]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
	<!-- Skins are provided by Renat Rafikov (2012). 
	     See http://simpliste.ru/en/ for more details. -->
      </head>
      <body>
	<div class="container">
	  <xsl:call-template name="show-header-default"/>

	  <xsl:call-template name="show-body"/>

	  <footer class="footer clearfix">
	    <div class="copyright">@2014 S.Gogolenko, Luxoft Odessa, CSS skins by Renat Rafikov</div>
	  </footer>
	</div>
      </body>
    </html>
  </xsl:template>

  <!-- ********************************************************* -->
  <!-- Customize HTML by choosing templates from the common list -->
  <!-- ********************************************************* -->
  <xsl:include href = "../nxUML/view/xslt/html/html-simple.xsl"/>
  <xsl:template name="show-project-logo">
    <a href="http://www.harman.com/EN-US/Pages/Home.aspx">
      <img src="css/logo/harman-logo.png" alt="MapCtrl logo" height="50"/>
    </a>
  </xsl:template>

  <xsl:include href = "../nxUML/view/xslt/common/feature.xsl"/>
  <xsl:include href = "../nxUML/view/xslt/html/html-summary.xsl"/>
  <xsl:template match="//attributes/attribute">
    <xsl:call-template name="show-attribute-tabular-summary-html"/>
  </xsl:template>
  <xsl:template match="//operations/operation">
    <xsl:call-template name="show-operation-tabular-summary-html"/>
  </xsl:template>

  <xsl:template match="//relationships/relationship[@direction='in']">
    <xsl:call-template name="show-in-relationship-item-html"/>
  </xsl:template>
  <xsl:template match="//relationships/relationship[@direction='out']">
    <xsl:call-template name="show-out-relationship-item-html"/>
  </xsl:template>

  <xsl:include href = "../nxUML/view/xslt/common/name.xsl"/>
  <xsl:template name="show-name">
    <xsl:call-template name="show-name-html"/>
  </xsl:template>
  <xsl:template name="show-reference">
    <xsl:call-template name="show-reference-html"/>
  </xsl:template>

  <xsl:include href = "../nxUML/view/xslt/common/visibility.xsl"/>
  <xsl:template name="show-visibility">
    <xsl:call-template name="show-visibility-img"/>
  </xsl:template>
  
  <xsl:include href = "../nxUML/view/xslt/common/multiplicity.xsl"/>
  <xsl:template name="show-multiplicities">
    <xsl:call-template name="show-multiplicity-img"/>
  </xsl:template>

  <xsl:include href = "../nxUML/view/xslt/common/property.xsl"/>
  <xsl:template name="show-modifiers">
    <xsl:call-template name="show-modifiers-img"/>
  </xsl:template>

  <xsl:template name="show-description">
    <xsl:choose>
      <xsl:when test="./@description">
	<xsl:value-of select="@description"/>
      </xsl:when>
      <xsl:otherwise>
	<i>No decsription</i>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
