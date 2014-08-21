<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl">
  
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  
  <xsl:template match="/class">
    <xsl:call-template name="show-html-default"/>
  </xsl:template>

  <xsl:template match="/interface">
    <xsl:call-template name="show-html-default"/>
  </xsl:template>

  <xsl:template match="/package">
    <xsl:call-template name="show-html-default"/>
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
      <xsl:for-each select="brownie">
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
      </xsl:for-each>
      <div class="clearfix"></div>

      <xsl:if test="relationship[@type='brownie::usage']">
	<h4>Require (concretes):</h4>
	<ul>
	  <xsl:apply-templates select="relationship[@type='brownie::usage']"/>
	</ul>
      </xsl:if>
      <xsl:if test="relationship[@type='brownie::realization']">
	<h4><span id="Brownie_provide">Provide (formals):</span> </h4>
	<ul>
	  <xsl:apply-templates select="relationship[@type='brownie::realization']"/>
	</ul>
      </xsl:if>
    </div>
  </xsl:template>

  <xsl:include href = "./brownie-common-html.xsl"/>
  <xsl:template name="show-body">
    <xsl:choose>
      <xsl:when test="name(.)='class'">
	<xsl:call-template name="show-body-class-default"/>
      </xsl:when>
      <xsl:when test="name(.)='interface'">
	<xsl:call-template name="show-body-class-default"/>
      </xsl:when>
      <xsl:when test="name(.)='package'">
	<xsl:call-template name="show-body-package-default"/>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
