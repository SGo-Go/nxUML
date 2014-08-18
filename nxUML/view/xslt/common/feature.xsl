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

  <xsl:template name="show-attribute-tabular-summary-html">
    <tr>
      <td align="right" valign="top" width="25%">
	<xsl:for-each select="datatype">
	  <xsl:call-template name="show-reference"/>
	  <xsl:call-template name="show-multiplicities"/>
	  <xsl:call-template name="show-properties"/>
	</xsl:for-each>
      </td>
      <td align="left" valign="top" width="25%">
	<xsl:call-template name="show-visibility"/>
	<xsl:call-template name="show-name"/>
      </td>
      <td>
	<xsl:call-template name="show-description"/>
      </td>
    </tr>
  </xsl:template>

  <xsl:template name="show-attribute-signature">
    <xsl:call-template name="show-visibility"/>
    <xsl:call-template name="show-name"/>
    <xsl:for-each select="datatype">
      <xsl:call-template name="show-reference"/>
      <xsl:call-template name="show-multiplicities"/>
      <xsl:call-template name="show-properties"/>
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
