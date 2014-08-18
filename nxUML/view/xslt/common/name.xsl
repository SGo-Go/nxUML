<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <xsl:template name="show-name-html">
    <span>
      <xsl:attribute name="title">
	<xsl:if test="@scope != '' ">
	  <xsl:value-of select="@scope"/>.<xsl:value-of select="./text()"/>
	</xsl:if>
      </xsl:attribute>
      <code><xsl:value-of select="text()"/></code>
    </span>
  </xsl:template>

  <xsl:template name="show-name-plain">
    <xsl:value-of select="text()"/>
  </xsl:template>

  <xsl:template name="show-reference-html">
    <xsl:choose>
      <xsl:when test="./@hrefId">
	<a>
	  <xsl:attribute name="href">
	    <xsl:call-template name="show-reference-url"/>
	  </xsl:attribute>
	  <xsl:call-template name="show-name"/>
	</a>
      </xsl:when>
      <xsl:otherwise>
	<xsl:call-template name="show-name"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="show-reference-url">
    <xsl:value-of select="@hrefId" />.html
  </xsl:template>

</xsl:stylesheet>
