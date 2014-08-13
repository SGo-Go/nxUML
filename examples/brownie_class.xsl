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
	<title>MapCtrl documentation [<xsl:value-of select="text()"/>]</title>
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
		<!-- <li><a href="#Brownie_provide">Brownie</a></li> -->
	      </ul>
	    </nav>
	  </header>

	  <div class="info">
	    <article class="hero clearfix">
	      <div class="col_100">
		<h1><xsl:value-of select="text()"/></h1>
		<big><code><xsl:apply-templates select="scope"/></code></big>

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
		  <li><a href="#methods">Methods</a></li>
		  <!-- <li><a href="#Brownie">Brownie</a></li> -->
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
      <xsl:call-template name="show-multiplicity" />
      <xsl:value-of select="@properties"/>
    </xsl:if>
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

  <xsl:template match="class/attributes/attribute">
    <tr>
      <td align="right" valign="top" width="25%">
	<xsl:apply-templates select="datatype"/>
      </td>
      <td align="left" valign="top" width="25%">
	<xsl:call-template name="show-visibility"/>
	<code><xsl:value-of select="text()"/></code>
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
	  <th>Return type</th>
	  <th>Name</th>
	</tr>
	<xsl:apply-templates select="method">
          <xsl:sort select="text()" />
        </xsl:apply-templates>
      </table>      
    </div>
  </xsl:template>
  <xsl:template match="class/methods[not(method)]">
  </xsl:template>

  <xsl:template match="class/methods/method">
    <tr>
      <td align="right" valign="top" width="25%">
	<xsl:apply-templates select="datatype"/>
      </td>
      <td>
	<xsl:call-template name="show-visibility"/>
	<code>
	  <xsl:choose>
	    <xsl:when test="./@abstract = 'yes' ">
	      <i><xsl:value-of select="text()"/></i>
	      <!-- = 0 -->
	    </xsl:when>
	    <xsl:otherwise>
	      <xsl:value-of select="text()"/>
	    </xsl:otherwise>
	  </xsl:choose>
	  </code>(<xsl:apply-templates select="parameter"/>)
	<xsl:value-of select="@properties"/>
	<br/>
	<xsl:call-template name="show-description"/>
      </td>
    </tr>
  </xsl:template>

  <xsl:template match="class/methods/method/parameter">
    <code><xsl:value-of select="text()"/></code> : <xsl:apply-templates select="datatype"/>, 
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

  <xsl:template name="brownie-relationships">
    <!-- <h2><span id="Brownie">Brownie interfaces</span></h2> -->

    <div class="col_100">
      <h4>Require (concretes):</h4>
      <!-- <table class="table"> -->
	<!-- <tr> -->
	<!--   <th>Name</th> -->
	<!--   <th>Class</th> -->
	<!-- </tr> -->
	<!-- <tr><th colspan = "2">Notifications</th></tr> -->
	<ul>
	  <xsl:apply-templates select="relationship[@type='brownie::usage']"/>
	</ul>
      <!-- 	<tr><th colspan = "2">Calls</th></tr> -->
      <!-- 	<xsl:apply-templates select="relationship[@type='brownie::usage']"/> -->
      <!-- </table> -->
    </div>

    <div class="col_100">
      <h4><span id="Brownie_provide">Provide (formals):</span> </h4>
      <!-- <table class="table"> -->
      <!-- 	<tr> -->
      <!-- 	  <th>Name</th> -->
      <!-- 	  <th>Class</th> -->
      <!-- 	</tr> -->
      <!-- 	<tr> -->
      <!-- 	  <th colspan = "2"> -->
      <!-- 	    Notifications -->
      <!-- 	  </th> -->
      <!-- 	</tr> -->
      <ul>
	<xsl:apply-templates select="relationship[@type='brownie::realization']"/>
      </ul>
      <!-- 	<tr> -->
      <!-- 	  <th colspan = "2"> -->
      <!-- 	    Calls -->
      <!-- 	  </th> -->
      <!-- 	</tr> -->
      <!-- 	<xsl:apply-templates select="relationship[@type='brownie::realization']"/> -->
      <!--   </table> -->
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

    <h3>Brownie</h3>
    <xsl:apply-templates select="brownie"/>
    <xsl:call-template name="brownie-relationships"/>

    <xsl:call-template name="inheritance-relationships"/>

    <!-- <xsl:apply-templates select="aggregations"/> -->

  </xsl:template>

  <!-- ************************************************** -->
  <!-- Brownie relationships templates -->
  <!-- ************************************************** -->
  <xsl:template match="class/relationships/brownie">
    <div class="col_100">
      <table class="table">
	<tr>
	  <xsl:for-each select="relationship">
	    <th class="message"><xsl:value-of select="@type"/></th>
	  </xsl:for-each>
	</tr>
	<tr>
	  <xsl:for-each select="relationship">
	    <td class="message"><code><xsl:apply-templates select="datatype[2]"/></code></td>
	  </xsl:for-each>
	</tr>
      </table>      
    </div>
    <div class="clearfix"></div>
    <!-- <td class="button"><xsl:value-of select="@type"/></td> -->
    <!-- <td><p class="message"><xsl:value-of select="@type"/></p></td> -->
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
	<xsl:call-template name="show-visibility"/>
	<code><xsl:apply-templates select="./datatype[1]"/></code>
      </td>
      <td><code><xsl:value-of select="@role"/></code></td>
    </tr>
  </xsl:template>

  <xsl:template match="class/relationships/aggregations/attribute">
    <tr>
      <td>
	<xsl:call-template name="show-visibility"/>
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
  <xsl:template name="inheritance-relationships">
    <div class="col_100">
      <h3>Inheritance</h3>
      <!-- <table class="table"> -->
      <!-- 	<tr> -->
      <!-- 	  <th>Class</th> -->
      <!-- 	  <th>Scope</th> -->
      <!-- 	</tr> -->
      <!-- <tr> -->
      <!--   <th colspan = "2"> -->
      <!--     Base classes -->
      <!--   </th> -->
      <!-- </tr> -->
      <h4>Extends:</h4> 
      <ul>
	<xsl:apply-templates select="relationship[@type='generalization' and @direction='out']"/>
      </ul>

      <h4>Derived:</h4> 
      <ul>
	<xsl:apply-templates select="relationship[@type='generalization' and @direction='in']"/>
      </ul>
      <!-- <tr> -->
      <!--   <th colspan = "2"> -->
      <!--     Derived classes -->
      <!--   </th> -->
      <!-- </tr> -->
      <!-- <xsl:apply-templates select="relationship[@direction='derived']"/> -->
      <!-- </table> -->
    </div>
  </xsl:template>

  <xsl:template match="class/relationships/relationship[@direction='in']">
    <!-- <tr> -->
    <!--   <td> -->
    <li>
      <xsl:call-template name="show-visibility"/>
      <code><xsl:apply-templates select="./datatype[1]"/></code>
    </li>
    <!--   </td> -->
    <!--   <td><code><xsl:value-of select="./datatype[2]/@scope"/></code></td> -->
    <!-- </tr> -->
  </xsl:template>

  <xsl:template match="class/relationships/relationship[@direction='out']">
    <!-- <tr> -->
    <!--   <td> -->
    <li>
      <xsl:call-template name="show-visibility"/>
      <code><xsl:apply-templates select="./datatype[2]"/></code>
    </li>
    <!--   </td> -->
    <!--   <td><code><xsl:value-of select="./datatype[2]/@scope"/></code></td> -->
    <!-- </tr> -->
  </xsl:template>

  <!-- <xsl:template match="class/relationships/relationship[@type='brownie::realization']"> -->
  <!--   <tr> -->
  <!--     <td> -->
  <!-- 	<xsl:call-template name="show-visibility"/> -->
  <!-- 	<code><xsl:apply-templates select="./datatype[2]"/></code> -->
  <!--     </td> -->
  <!--     <td><code><xsl:value-of select="./datatype[2]/@scope"/></code></td> -->
  <!--   </tr> -->
  <!-- </xsl:template> -->

  <!-- <xsl:template match="class/relationships/relationship[@direction='base']"> -->
  <!--   <tr> -->
  <!--     <td> -->
  <!-- 	<xsl:call-template name="show-visibility"/> -->
  <!-- 	<code><xsl:apply-templates select="./datatype[2]"/></code> -->
  <!--     </td> -->
  <!--     <td><code><xsl:value-of select="./datatype[2]/@scope"/></code></td> -->
  <!--   </tr> -->
  <!-- </xsl:template> -->

  <!-- <xsl:template match="class/relationships/inheritances/relationship[@direction='derived']"> -->
  <!--   <tr> -->
  <!--     <td> -->
  <!-- 	<xsl:call-template name="show-visibility"/> -->
  <!-- 	<code><xsl:apply-templates select="./datatype[1]"/></code> -->
  <!--     </td> -->
  <!--     <td><code><xsl:value-of select="./datatype[1]/@scope"/></code></td> -->
  <!--   </tr> -->
  <!-- </xsl:template> -->

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

  <xsl:template match="scope">
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
	<xsl:value-of select="text()"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>


  <!-- <xsl:call-template name="put-reference"/> -->

  <!-- ************************************************** -->
  <!-- Common icons -->
  <!-- ************************************************** -->

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

  <xsl:template name="show-visibility">
      <xsl:choose>
	<xsl:when test="./@visibility = '-'">
	  <span title='private'><img src="css/icons/privattr.gif" alt="-" /></span>
	</xsl:when>
	<xsl:when test="./@visibility = '+'">
	  <span title='public'><img src="css/icons/publattr.gif" alt="+" /></span>
	</xsl:when>
	<xsl:when test="./@visibility = '#'">
	  <span title='protected'><img src="css/icons/protattr.gif" alt="#" /></span>
	</xsl:when>

	<xsl:when test="./@visibility = '- '">
	  <span title='private'><img src="css/icons/privoper.gif" alt="- " /></span>
	</xsl:when>
	<xsl:when test="./@visibility = '+ '">
	  <span title='public'><img src="css/icons/publoper.gif" alt="+ " /></span>
	</xsl:when>
	<xsl:when test="./@visibility = '# '">
	  <span title='protected'><img src="css/icons/protoper.gif" alt="# " /></span>
	</xsl:when>

	<xsl:when test="./@visibility = '-/'">
	  <span title='private virtual'><img src="css/icons/virtprivoper.gif" alt="-/" /></span>
	</xsl:when>
	<xsl:when test="./@visibility = '+/'">
	  <span title='public virtual'><img src="css/icons/virtpubloper.gif" alt="+/" /></span>
	</xsl:when>
	<xsl:when test="./@visibility = '#/'">
	  <span title='protected virtual'><img src="css/icons/virtprotoper.gif" alt="#/" /></span>
	</xsl:when>

	<xsl:otherwise>
	  <xsl:value-of select="./@visibility"/>
	</xsl:otherwise>
      </xsl:choose>
  </xsl:template>

  <xsl:template name="show-multiplicity">
    <xsl:for-each select="multiplicity">
      <xsl:choose>
	<xsl:when test="./@type = 'pointer'">
	  <span title='pointer'><img src="css/icons/pointer.gif" alt="&#x27AE;" /></span><!-- &#x21B3 x27AE-->
	</xsl:when>

	<xsl:when test="./@type = 'reference'">
	  <span title='reference'><img src="css/icons/reference.png" alt="&amp;" /></span>
	</xsl:when>

	<xsl:when test="./@type = 'quantifier'">
	  <span>
	    <xsl:attribute name="title">
    	      quantifier:
	      <xsl:value-of select="./@bind"/>(key=<xsl:value-of select="./@key"/>)
    	    </xsl:attribute>
	    <img src="css/icons/qualifier.gif" alt="&#x272A;" />
	  </span> <!-- 2605 -->
	  <sup><b><xsl:value-of select="./@bind"/></b>(key=<xsl:value-of select="./@key"/>)</sup>
	</xsl:when>

	<xsl:otherwise>
	  <xsl:value-of select="./@multiplicity"/>
	</xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
