<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl">
  
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  
  <xsl:template match="/class">
    <html lang="en">
      <head>
	<meta charset="utf-8"/>
	<meta name="viewport" content="width=device-width,initial-scale=1"/>
	<!-- <link href="favicon.ico" rel="shortcut icon"/> -->
	<link rel="stylesheet" href="css/style.css"/>
	<title>MapCtrl documentation</title>
	<!--[if lt IE 9]><script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
	<!-- Skins are provided by Renat Rafikov (2012). 
	     See http://simpliste.ru/en/ for more details. -->
      </head>
      <body>
	<div class="container">
	  <header class="header clearfix">
	    <div class="logo"><img src="css/logo/harman-logo.png" alt="MapCtrl logo" height="50"/></div>
	    <nav class="menu_main">
	      <ul>
		<li><a href="#">Main</a></li>
		<li><a href="#">Header</a></li>
		<li class="active"><a href="#">Class</a></li>
		<li><a href="#Brownie_provide">Brownie</a></li>
	      </ul>
	    </nav>
	  </header>

	  <div class="info">
	    <article class="hero clearfix">
	      <div class="col_100">
		<h1><xsl:value-of select="text()"/></h1>
		<big><code><xsl:value-of select="@scope"/></code></big>

		<h2>Description</h2>
		<p>
		  <xsl:call-template name="show-description"/>
		</p>
	      </div>
	      <nav class="menu_bottom">
		<ul>
		  <!-- <li class="active"><a href="#">Top</a></li> -->
		  <li><a href="#relationships">Relationships</a></li>
		  <li><a href="#attributes">Attributes</a></li>
		  <li><a href="#methods">Methods</a></li>
		  <li><a href="#Brownie">Brownie</a></li>
		</ul>
	      </nav>
	    </article>

	    <article class="article clearfix">

	      <xsl:apply-templates select="relationships"/>

	      <xsl:apply-templates select="attributes"/>

	      <xsl:apply-templates select="methods"/>

	      <xsl:apply-templates select="interfaces"/>

	    </article>
	  </div>

	  <footer class="footer clearfix">
	    <div class="copyright">@2014 S.Gogolenko, Luxoft Odessa, CSS skins by Renat Rafikov</div>
	  </footer>
	</div>
      </body>
    </html>
  </xsl:template>

  <!-- <xsl:template match="class/attributes/attribute/datatype"> -->
  <!--   <code><xsl:value-of select="text()"/></code><xsl:value-of select="@multiplicity"/> -->
  <!-- </xsl:template> -->

  <xsl:template match="class/*/*/datatype">
    <xsl:if test="text() != '' ">
      <code><xsl:call-template name="put-reference"/></code>
      <xsl:value-of select="@multiplicity"/>
      <xsl:value-of select="@properties"/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="class/attributes">
    <div class="col_100">
      <h2><span id="attributes">Attributes</span></h2>
      <table class="table">
	<tr>
	  <th>Name</th>
	  <th>Type</th>
	  <th>Description</th>
	</tr>
	<xsl:apply-templates select="attribute"/>
      </table>      
    </div>
  </xsl:template>
  <xsl:template match="class/attributes[not(attribute)]">
  </xsl:template>

  <xsl:template match="class/attributes/attribute">
    <tr>
      <td>
	<xsl:value-of select="@visibility"/>
	<code><xsl:value-of select="text()"/></code>
      </td>
      <td>
	<xsl:apply-templates select="datatype"/>
      </td>
      <td>
	<xsl:call-template name="show-description"/>
      </td>
    </tr>
  </xsl:template>


  <xsl:template match="class/methods">
    <div class="col_100">
      <h2><span id="methods">Methods</span></h2>
      <table class="table">
	<tr>
	  <th>Name</th>
	  <th>Return type</th>
	  <th>Description</th>
	</tr>
	<xsl:apply-templates select="method"/>
      </table>      
    </div>
  </xsl:template>
  <xsl:template match="class/methods[not(method)]">
  </xsl:template>

  <xsl:template match="class/methods/method">
    <tr>
      <td>
	<xsl:value-of select="@visibility"/>
	<code><xsl:value-of select="text()"/>()</code>
	<xsl:choose>
	  <xsl:when test="./@abstract = 'yes' ">
	    = 0
	  </xsl:when>
	  <xsl:otherwise>
	  </xsl:otherwise>
	</xsl:choose>
	<xsl:value-of select="@properties"/>
      </td>
      <td>
	<xsl:apply-templates select="datatype"/>
      </td>
      <td>
	<xsl:call-template name="show-description"/>
      </td>
    </tr>
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


  <xsl:template match="class/interfaces">
    <h2><span id="Brownie">Brownie interfaces</span></h2>
    <xsl:apply-templates select="in"/>
    <xsl:apply-templates select="out"/>
  </xsl:template>

  <xsl:template match="class/interfaces/in">
    <div class="col_66">
      <h3>Require (Concretes) </h3>
      <table class="table">
	<tr>
	  <th>Name</th>
	  <th>Class</th>
	</tr>
	<tr><th colspan = "2">Notifications</th></tr>
	<xsl:apply-templates select="interface[@type='notification']"/>
	<tr><th colspan = "2">Calls</th></tr>
	<xsl:apply-templates select="interface[@type='call']"/>
      </table>      
    </div>
  </xsl:template>

  <xsl:template match="class/interfaces/out">
    <div class="col_66">
      <h3><span id="Brownie_provide">Provide (Formals)</span> </h3>
      <table class="table">
	<tr>
	  <th>Name</th>
	  <th>Class</th>
	</tr>
	<tr>
	  <th colspan = "2">
	    Notifications
	  </th>
	</tr>
	<xsl:apply-templates select="interface[@type='notification']"/>
	<tr>
	  <th colspan = "2">
	    Calls
	  </th>
	</tr>
	<xsl:apply-templates select="interface[@type='call']"/>
      </table>
    </div>
  </xsl:template>

  <xsl:template match="interface">
    <tr>
      <td>
	<code><xsl:value-of select="@name"/></code>
      </td>
      <td>
	<code><xsl:value-of select="@owner-name"/></code>
      </td>
    </tr>
  </xsl:template>

  <!-- ************************************************** -->
  <!-- Relationships templates -->
  <!-- ************************************************** -->

  <xsl:template match="class/relationships">
    <h2><span id="relationships">Relationships</span></h2>

    <xsl:apply-templates select="brownie"/>

    <xsl:apply-templates select="inheritances"/>

    <xsl:apply-templates select="aggregations"/>

  </xsl:template>

  <!-- ************************************************** -->
  <!-- Brownie relationships templates -->
  <!-- ************************************************** -->
  <xsl:template match="class/relationships/brownie">
    <div class="col_100">
      <h3>Brownie</h3>
      <table class="table">
	<tr>
	  <th>Relationship</th>
	  <th>Class</th>
	</tr>
	<xsl:apply-templates select="relationship"/>
      </table>      
    </div>
    <div class="clearfix"></div>
  </xsl:template>

  <xsl:template match="class/relationships/brownie/relationship">
    <tr>
      <td>
	<xsl:value-of select="@type"/>
      </td>
      <td>
	<code><xsl:apply-templates select="datatype[2]"/></code>
      </td>
    </tr>
  </xsl:template>

  <!-- ************************************************** -->
  <!-- Aggregations relationships templates -->
  <!-- ************************************************** -->
  <xsl:template match="class/relationships/aggregations">
    <div class="col_100">
      <h3>Aggregations</h3>
      <table class="table">
	<tr>
	  <th>Owner</th>
	  <th>Role (attribute name)</th>
	</tr>
	<xsl:apply-templates select="relationship[@direction='part']"/>
	<!-- <xsl:apply-templates select="attribute"/> -->
      </table>      
    </div>
  </xsl:template>

  <xsl:template match="class/relationships/aggregations/relationship[@direction='part']">
    <tr>
      <td>
	<xsl:value-of select="@visibility"/>
	<code><xsl:apply-templates select="./datatype[1]"/></code>
      </td>
      <td><code><xsl:value-of select="@role"/></code></td>
    </tr>
  </xsl:template>

  <xsl:template match="class/relationships/aggregations/attribute">
    <tr>
      <td>
	<xsl:value-of select="@visibility"/>
	<code><xsl:value-of select="@owner-name"/></code>
      </td>
      <td>
	<code><xsl:value-of select="text()"/></code>
      </td>
    </tr>
  </xsl:template>

  <!-- ************************************************** -->
  <!-- Inheritance relationships templates -->
  <!-- ************************************************** -->
  <xsl:template match="class/relationships/inheritances">
    <div class="col_100">
      <h3>Inheritances</h3>
      <table class="table">
	<tr>
	  <th>Class</th>
	  <th>Scope</th>
	</tr>
	<tr>
	  <th colspan = "2">
	    Base classes
	  </th>
	</tr>
	<xsl:apply-templates select="relationship[@direction='base']"/>
	<tr>
	  <th colspan = "2">
	    Derived classes
	  </th>
	</tr>
	<xsl:apply-templates select="relationship[@direction='derived']"/>
      </table>
    </div>
  </xsl:template>

  <xsl:template match="class/relationships/inheritances/relationship[@direction='base']">
    <tr>
      <td>
	<xsl:value-of select="@visibility"/>
	<code><xsl:apply-templates select="./datatype[1]"/></code>
      </td>
      <td><code><xsl:value-of select="./datatype[1]/@scope"/></code></td>
    </tr>
  </xsl:template>

  <xsl:template match="class/relationships/inheritances/relationship[@direction='derived']">
    <tr>
      <td>
	<xsl:value-of select="@visibility"/>
	<code><xsl:apply-templates select="./datatype[2]"/></code>
      </td>
      <td><code><xsl:value-of select="./datatype[2]/@scope"/></code></td>
    </tr>
  </xsl:template>

  <!-- ************************************************** -->
  <!-- Common templates -->
  <!-- ************************************************** -->
  <xsl:template match="class/*/*/*/datatype">
    <xsl:if test="text() != '' ">
      <code><xsl:call-template name="put-reference"/></code>
      <xsl:value-of select="@multiplicity"/>
      <xsl:value-of select="@properties"/>
    </xsl:if>
  </xsl:template>

  <!-- <xsl:call-template name="put-reference"/> -->

  <xsl:template name="put-reference">
      <xsl:choose>
	<xsl:when test="./@hrefId">
	  <a>
	    <xsl:attribute name="href">
	      <xsl:value-of select="@hrefId" />.html
	    </xsl:attribute>
	    <xsl:value-of select="text()"/>
	  </a>
	</xsl:when>
	<xsl:otherwise>
	  <xsl:if test="@scope != '' ">
	    <!-- [<xsl:value-of select="@scope"/>] -->
	  </xsl:if>
	  <xsl:value-of select="text()"/>
	</xsl:otherwise>
      </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
