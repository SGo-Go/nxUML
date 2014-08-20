<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <!-- ************************************************** -->
  <!-- Common templates -->
  <!-- ************************************************** -->
  <xsl:template match="datatype">
    <xsl:if test="text() != '' ">
      <xsl:call-template name="show-reference"/>
      <xsl:call-template name="show-multiplicities"/>
      <xsl:call-template name="show-properties"/>
    </xsl:if>
  </xsl:template>

  <xsl:template name="show-attribute-signature-full">
    <xsl:call-template name="show-visibility"/>
    <xsl:call-template name="show-name"/>
    <xsl:for-each select="datatype">
      <xsl:call-template name="show-reference"/>
      <xsl:call-template name="show-multiplicities"/>
      <xsl:call-template name="show-properties"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="show-attribute-signature-short">
    <xsl:call-template name="show-visibility"/>
    <xsl:call-template name="show-name"/>
  </xsl:template>

  <xsl:template name="show-operation-signature-full">
    <xsl:call-template name="show-visibility"/>
    <xsl:choose>
      <xsl:when test="./@abstract = 'yes' ">
	<i><xsl:call-template name="show-name"/></i>
      </xsl:when>
      <xsl:otherwise>
	<xsl:call-template name="show-name"/>
      </xsl:otherwise>
    </xsl:choose>
    (<xsl:for-each select="parameter">
    <xsl:call-template name="show-name"/>:<xsl:apply-templates select="datatype"/>
    <xsl:if test="not(position() = last())">, </xsl:if>
    </xsl:for-each>):<xsl:apply-templates select="datatype"/>
    <xsl:call-template name="show-properties"/>
  </xsl:template>

  <xsl:template name="show-operation-signature-short">
    <xsl:call-template name="show-visibility"/>
    <xsl:choose>
      <xsl:when test="./@abstract = 'yes' ">
	<i><xsl:call-template name="show-name"/></i>
      </xsl:when>
      <xsl:otherwise>
	<xsl:call-template name="show-name"/>
      </xsl:otherwise>
      </xsl:choose>()
      <xsl:apply-templates select="datatype"/>
  </xsl:template>
</xsl:stylesheet>
