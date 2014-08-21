<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <xsl:template match="class/attributes | interface/attributes">
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
  <xsl:template match="class/attributes[not(attribute)] | class/attributes[not(attribute)]">
  </xsl:template>


  <!-- ************************************************** -->
  <!-- Relationship lists templates -->
  <!-- ************************************************** -->
  <xsl:template name="inheritance-relationships">
    <xsl:if test="relationship[@type='generalization']">
      <div class="col_100">
	<h3>Inheritance</h3>
	<xsl:if test="relationship[@type='generalization' and @direction='out']">
	  <h4>Extends:</h4> 
	  <ul>
	    <xsl:apply-templates select="relationship[@type='generalization' and @direction='out']"/>
	  </ul>
	</xsl:if>

	<xsl:if test="relationship[@type='generalization' and @direction='in']">
	  <h4>Extended in:</h4> 
	  <ul>
	    <xsl:apply-templates select="relationship[@type='generalization' and @direction='in']"/>
	  </ul>
	</xsl:if>
      </div>
    </xsl:if>
  </xsl:template>


  <!-- ************************************************** -->
  <!-- Class features tables templates -->
  <!-- ************************************************** -->

  <xsl:template match="class/operations | interface/operations">
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
  <xsl:template match="class/operations[not(operation)]  | interface/operations[not(operation)]">
  </xsl:template>

  <!-- ********************************************************* -->
  <!-- List of nested elements  -->
  <!-- ********************************************************* -->
  <xsl:template match="//inner">
    <h2><span id="inner">Inner elements</span></h2>
    <ul>
      <!-- <xsl:for-each select="datatype[@type='class']"> -->
      <xsl:for-each select="datatype">
        <xsl:sort select="text()" />
	<li><xsl:call-template name="show-reference"/></li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template name="show-internal-menu">
    <nav class="menu_bottom">
      <ul>
	<xsl:if test="relationships">
	  <li><a href="#relationships">Relationships</a></li>
	</xsl:if>
	<xsl:if test="inner">
	  <li><a href="#inner">Inner</a></li>
	</xsl:if>
	<xsl:if test="attributes and attributes/attribute">
	  <li><a href="#attributes">Attributes</a></li>
	</xsl:if>
	<xsl:if test="operations and operations/operation">
	  <li><a href="#operations">Operations</a></li>
	</xsl:if>
      </ul>
    </nav>
  </xsl:template>

  <xsl:template name="show-main-menu">
    <nav class="menu_main">
      <ul>
	<li><a href="#">Main</a></li>
	<li><a href="#">Header</a></li>
	<li class="active"><a><xsl:call-template name="show-type-name"/></a></li>
      </ul>
    </nav>
  </xsl:template>

  <xsl:template name="show-top-button">
    <nav class="menu_bottom"><ul><li><a href="#">Top</a></li></ul></nav>
  </xsl:template>

  <xsl:template name="show-element-description-default">
    <article class="hero clearfix">
      <div class="col_100">
	<xsl:call-template name="show-title"/>

	<xsl:if test="scope != '' ">
	  <xsl:for-each select="scope">
	    <big>
	      <xsl:for-each select="datatype">
		<xsl:call-template name="show-reference"/>
		<xsl:if test="not(position() = last())">.</xsl:if>
	      </xsl:for-each>
	    </big>
	  </xsl:for-each>
	</xsl:if>

	<h2>Overview</h2>
	<p>
	  <xsl:call-template name="show-description"/>
	</p>
      </div>
      
      <xsl:call-template name="show-internal-menu"/>
    </article>
  </xsl:template>

  <xsl:template name="show-project-logo-default">
    <huge>Project</huge>
  </xsl:template>

  <xsl:template name="show-header-default">
    <header class="header clearfix">
      <div class="logo">
	<xsl:call-template name="show-project-logo"/>
      </div>
      <xsl:call-template name="show-main-menu"/>
    </header>
  </xsl:template>

  <xsl:template name="show-body-class-default">
    <div class="info">
      <xsl:call-template name="show-element-description-default"/>

      <article class="article clearfix">
	<xsl:if test="relationships">
	  <xsl:apply-templates select="relationships"/>
	  <xsl:call-template name="show-top-button"/>
	</xsl:if>

	<xsl:if test="inner">
	  <xsl:apply-templates select="inner"/>
	  <xsl:call-template name="show-top-button"/>
	</xsl:if>

	<xsl:if test="attributes and attributes/attribute">
	  <xsl:apply-templates select="attributes"/>
	  <xsl:call-template name="show-top-button"/>
	</xsl:if>

	<xsl:if test="operations and operations/operation">
	  <xsl:apply-templates select="operations"/>
	  <xsl:call-template name="show-top-button"/>
	</xsl:if>
      </article>
    </div>
  </xsl:template>

  <xsl:template name="show-body-package-default">
    <div class="info">
      <xsl:call-template name="show-element-description-default"/>

      <article class="article clearfix">
	<xsl:if test="relationships">
	  <xsl:apply-templates select="relationships"/>
	  <xsl:call-template name="show-top-button"/>
	</xsl:if>

	<xsl:if test="inner">
	  <xsl:apply-templates select="inner"/>
	  <xsl:call-template name="show-top-button"/>
	</xsl:if>
      </article>
    </div>
  </xsl:template>


  <xsl:template name="show-title">
    <h1><xsl:call-template name="show-type-name"/> <!-- &#xA0; -->
    <xsl:text> </xsl:text>
    <xsl:call-template name="show-name"/>
    </h1>
  </xsl:template>

  <xsl:template name="show-type-name">
    <xsl:value-of select="name(.)"/>
  </xsl:template>

</xsl:stylesheet>
