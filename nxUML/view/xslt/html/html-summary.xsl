<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <!-- ************************************************** -->
  <!-- Common templates -->
  <!-- ************************************************** -->

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

  <xsl:template name="show-operation-tabular-summary-html">
    <tr>
      <td align="right" valign="top" width="25%">
	<xsl:for-each select="datatype">
	  <xsl:call-template name="show-reference"/>
	  <xsl:call-template name="show-multiplicities"/>
	  <xsl:call-template name="show-properties"/>
	</xsl:for-each>
      </td>
      <td>
	<xsl:call-template name="show-visibility"/>
	<xsl:choose>
	  <xsl:when test="./@abstract = 'yes' ">
	    <i><xsl:call-template name="show-name"/></i>
	    <!-- = 0 -->
	  </xsl:when>
	  <xsl:otherwise>
	    <xsl:call-template name="show-name"/>
	  </xsl:otherwise>
	</xsl:choose>
	(<xsl:for-each select="parameter">
	<xsl:call-template name="show-name"/>:<xsl:apply-templates select="datatype"/>
	<xsl:if test="not(position() = last())">, </xsl:if>
	</xsl:for-each>)
	<xsl:call-template name="show-properties"/>
	<br/>
	<xsl:call-template name="show-description"/>
      </td>
    </tr>
  </xsl:template>

  <xsl:template name="show-in-relationship-item-html">
    <li>
      <xsl:call-template name="show-visibility"/>
      <xsl:apply-templates select="./datatype[1]"/>
    </li>
  </xsl:template>

  <xsl:template name="show-out-relationship-item-html">
    <li>
      <xsl:call-template name="show-visibility"/>
      <xsl:apply-templates select="./datatype[2]"/>
    </li>
  </xsl:template>

</xsl:stylesheet>
