<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <xsl:template match="//attributes">
    --
    <xsl:apply-templates select="attribute[datatype[1]/@type='class']">
      <xsl:sort select="datatype[1]/text()" />
    </xsl:apply-templates>
  </xsl:template>
  <xsl:template match="//attributes[not(attribute)]">
  </xsl:template>

  <!-- ************************************************** -->
  <!-- Class features tables templates -->
  <!-- ************************************************** -->

  <xsl:template match="//operations">
    <xsl:apply-templates select="operation">
      <xsl:sort select="text()" />
    </xsl:apply-templates>
  </xsl:template>
  <xsl:template match="//operations[not(operation)]">
  </xsl:template>

  <xsl:template name="show-body-class-default">
    <element>
      <type>com.umlet.element.Class</type>

      <xsl:call-template name="show-coordinates"/>
      <panel_attributes>
	<xsl:choose>
	  <xsl:when test="./@abstract = 'yes' ">
	    <i><xsl:call-template name="show-name"/></i>
	  </xsl:when>
	  <xsl:otherwise>
	    <xsl:call-template name="show-name"/>
	  </xsl:otherwise>
	</xsl:choose>&#160;
	--&#160;
	<xsl:apply-templates select="attributes"/>--&#160;
	<xsl:apply-templates select="operations"/>
      </panel_attributes>
    </element>
  </xsl:template>

</xsl:stylesheet>
