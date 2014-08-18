<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl">
  
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  
  <xsl:template match="/class">
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
	  <header class="header clearfix">
	    <div class="logo"><a href="http://www.harman.com/EN-US/Pages/Home.aspx">
	      <img src="css/logo/harman-logo.png" alt="MapCtrl logo" height="50"/>
	    </a></div>
	    <nav class="menu_main">
	      <ul>
		<li><a href="#">Main</a></li>
		<li><a href="#">Header</a></li>
		<li class="active"><a href="#">Class</a></li>
		<!-- <li><a href="#Brownie_provide">Brownie</a></li> -->
	      </ul>
	    </nav>
	  </header>

	  <div class="info">
	    <article class="hero clearfix">
	      <div class="col_100">
		<h1><xsl:call-template name="show-name"/></h1>
		<xsl:if test="scope != '' ">
		  <big><code>
		    <xsl:apply-templates select="scope"/>
		  </code></big>
		</xsl:if>

		<h2>Class Overview</h2>
		<p>
		  <xsl:call-template name="show-description"/>
		</p>
	      </div>
	      <nav class="menu_bottom">
		<ul>
		  <!-- <li class="active"><a href="#">Top</a></li> -->
		  <li><a href="#relationships">Relationships</a></li>
		  <li><a href="#attributes">Attributes</a></li>
		  <li><a href="#operations">Operations</a></li>
		  <!-- <li><a href="#Brownie">Brownie</a></li> -->
		</ul>
	      </nav>
	    </article>

	    <article class="article clearfix">

	      <xsl:apply-templates select="relationships"/>

	      <xsl:apply-templates select="nested"/>

	      <xsl:apply-templates select="attributes"/>

	      <xsl:apply-templates select="operations"/>

	    </article>
	  </div>

	  <footer class="footer clearfix">
	    <div class="copyright">@2014 S.Gogolenko, Luxoft Odessa, CSS skins by Renat Rafikov</div>
	  </footer>
	</div>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="class/attributes">
    <div class="col_100">
      <h2><span id="attributes">Attributes</span></h2>
      <table class="table">
	<tr>
	  <th>Type</th>
	  <th>Name</th>
	  <th>Description</th>
	</tr>
	<xsl:copy>
	  <tr><th colspan="3">Primitive [<xsl:number value="count(attribute[datatype[1]/@type='primitive'])"/>]</th></tr>
	  <xsl:apply-templates select="attribute[datatype[1]/@type='primitive']">
            <xsl:sort select="datatype[1]/text()" />
          </xsl:apply-templates>
	  <tr><th colspan="3">Simple [<xsl:number value="count(attribute[not(datatype[1]/@type)])"/>]</th></tr>
	  <xsl:apply-templates select="attribute[not(datatype[1]/@type)]">
            <xsl:sort select="datatype[1]/text()" />
          </xsl:apply-templates>
	  <tr><th colspan="3">Classes [<xsl:number value="count(attribute[datatype[1]/@type='class'])"/>]</th></tr>
	  <xsl:apply-templates select="attribute[datatype[1]/@type='class']">
            <xsl:sort select="datatype[1]/text()" />
          </xsl:apply-templates>
	</xsl:copy>
      </table>
    </div>
  </xsl:template>
  <xsl:template match="class/attributes[not(attribute)]">
  </xsl:template>

  <xsl:template match="class/operations">
    <div class="col_100">
      <h2><span id="operations">Operations</span></h2>
      <table class="table">
	<tr>
	  <th>Return type</th>
	  <th>Name</th>
	</tr>
	<xsl:apply-templates select="operation">
          <xsl:sort select="text()" />
        </xsl:apply-templates>
      </table>      
    </div>
  </xsl:template>
  <xsl:template match="class/operations[not(operation)]">
  </xsl:template>

  <xsl:template match="class/operations/operation">
    <tr>
      <td align="right" valign="top" width="25%">
	<xsl:apply-templates select="datatype"/>
      </td>
      <td>
	<xsl:call-template name="show-visibility"/>
	  <xsl:choose>
	    <xsl:when test="./@abstract = 'yes' ">
	      <i><xsl:call-template name="show-name"/></i>
	      <!-- = 0 -->
	    </xsl:when>
	    <xsl:otherwise>
	      <xsl:call-template name="show-name"/>
	    </xsl:otherwise>
	  </xsl:choose>
	  (<xsl:apply-templates select="parameter"/>)
	  <xsl:call-template name="show-properties"/>
	  <br/>
	  <xsl:call-template name="show-description"/>
      </td>
    </tr>
  </xsl:template>

  <xsl:template match="operations/operation/parameter">
    <xsl:call-template name="show-name"/> : <xsl:apply-templates select="datatype"/>, 
  </xsl:template>

  <!-- ************************************************** -->
  <!-- Relationships templates -->
  <!-- ************************************************** -->

  <xsl:template match="class/relationships">
    <h2><span id="relationships">Relationships</span></h2>
    <xsl:call-template name="brownie-relationships"/>
    <xsl:call-template name="inheritance-relationships"/>
    <!-- <xsl:apply-templates select="aggregations"/> -->
  </xsl:template>

  <!-- ************************************************** -->
  <!-- Brownie relationships templates -->
  <!-- ************************************************** -->
  <xsl:template name="brownie-relationships">
    <h3>Brownie</h3>
    <div class="col_100">
      <xsl:apply-templates select="brownie"/>
      <div class="clearfix"></div>

      <h4>Require (concretes):</h4>
      <ul>
	<xsl:apply-templates select="relationship[@type='brownie::usage']"/>
      </ul>
      <h4><span id="Brownie_provide">Provide (formals):</span> </h4>
      <ul>
	<xsl:apply-templates select="relationship[@type='brownie::realization']"/>
      </ul>
    </div>
  </xsl:template>

  <xsl:template match="class/relationships/brownie">
      <table class="table">
	<tr>
	  <xsl:for-each select="relationship">
	    <th class="message"><xsl:value-of select="@type"/></th>
	  </xsl:for-each>
	</tr>
	<tr>
	  <xsl:for-each select="relationship">
	    <td class="message"><xsl:apply-templates select="datatype[2]"/></td>
	  </xsl:for-each>
	</tr>
      </table>      
  </xsl:template>

  <xsl:template match="class/relationships/brownie/relationship">
    <tr>
      <td>
	<xsl:value-of select="@type"/>
      </td>
      <td>
	<xsl:apply-templates select="datatype[2]"/>
      </td>
    </tr>
  </xsl:template>

  <!-- ************************************************** -->
  <!-- Inheritance relationships templates -->
  <!-- ************************************************** -->
  <xsl:template name="inheritance-relationships">
    <div class="col_100">
      <h3>Inheritance</h3>
      <h4>Extends:</h4> 
      <ul>
	<xsl:apply-templates select="relationship[@type='generalization' and @direction='out']"/>
      </ul>

      <h4>Derived:</h4> 
      <ul>
	<xsl:apply-templates select="relationship[@type='generalization' and @direction='in']"/>
      </ul>
    </div>
  </xsl:template>

  <xsl:template match="class/relationships/relationship[@direction='in']">
    <li>
      <xsl:call-template name="show-visibility"/>
      <xsl:apply-templates select="./datatype[1]"/>
    </li>
  </xsl:template>

  <xsl:template match="class/relationships/relationship[@direction='out']">
    <li>
      <xsl:call-template name="show-visibility"/>
      <xsl:apply-templates select="./datatype[2]"/>
    </li>
  </xsl:template>

  <xsl:template match="scope">
    <!-- <xsl:call-template name="show-reference"/> -->
    <xsl:choose>
      <xsl:when test="./@hrefId">
    	<a>
    	  <xsl:attribute name="href">
    	    <xsl:value-of select="@hrefId" />.html
    	  </xsl:attribute>
    	  <xsl:call-template name="show-name"/>
    	</a>
      </xsl:when>
      <xsl:otherwise>
    	<xsl:call-template name="show-name"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- ********************************************************* -->
  <!-- Customize HTML by choosing templates from the common list -->
  <!-- ********************************************************* -->
  <xsl:include href = "../nxUML/view/xslt/common/feature.xsl"/>
  <xsl:template match="class/attributes/attribute">
    <xsl:call-template name="show-attribute-tabular-summary-html"/>
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
  <xsl:template name="show-properties">
    <xsl:call-template name="show-properties-img"/>
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
