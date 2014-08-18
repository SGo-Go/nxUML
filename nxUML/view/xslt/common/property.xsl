<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <xsl:template name="show-properties-img">
    <xsl:value-of select="./@properties"/>
  </xsl:template>

  <xsl:template name="show-properties-unicode">
    <xsl:value-of select="./@properties"/>
  </xsl:template>

  <xsl:template name="show-properties-plain">
    <xsl:value-of select="./@properties"/>
  </xsl:template>

</xsl:stylesheet>
