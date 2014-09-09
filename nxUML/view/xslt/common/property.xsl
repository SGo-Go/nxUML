<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <xsl:template name="show-modifiers-img">
    <xsl:value-of select="./@modifiers"/>
  </xsl:template>

  <xsl:template name="show-modifiers-unicode">
    <xsl:value-of select="./@modifiers"/>
  </xsl:template>

  <xsl:template name="show-modifiers-plain">
    <xsl:value-of select="./@modifiers"/>
  </xsl:template>

</xsl:stylesheet>
