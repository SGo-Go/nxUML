<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <xsl:template name="show-multiplicity-img">
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

  <xsl:template name="show-multiplicity-unicode">
    <xsl:for-each select="multiplicity">
      <xsl:choose>
	<xsl:when test="./@type = 'pointer'">
	  <span title='pointer'><font color="cyan">&#x24C5;</font></span><!-- &#x21B3 x27AE-->
	</xsl:when>

	<xsl:when test="./@type = 'reference'">
	  <span title='reference'><font color="cyan">&#x24C7;</font></span>
	</xsl:when>

	<xsl:when test="./@type = 'quantifier'">
	  <span>
	    <xsl:attribute name="title">
    	      quantifier:
	      <xsl:value-of select="./@bind"/>(key=<xsl:value-of select="./@key"/>)
    	    </xsl:attribute>
	    <font color="cyan">&#x24C6;</font>
	  </span> <!-- 2605 -->
	  <sup><b><xsl:value-of select="./@bind"/></b>(key=<xsl:value-of select="./@key"/>)</sup>
	</xsl:when>

	<xsl:otherwise>
	  <xsl:value-of select="./@multiplicity"/>
	</xsl:otherwise>
      </xsl:choose>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="show-multiplicity-plain">
    <xsl:for-each select="multiplicity">
      <!-- <xsl:choose> -->
      <!-- 	<xsl:when test="./@type = 'quantifier'"> -->
      <!-- 	  <xsl:value-of select="./@bind"/>(key=<xsl:value-of select="./@key"/>) -->
      <!-- 	</xsl:when> -->
      <!-- 	<xsl:otherwise> -->
      <xsl:value-of select="./text()"/>
      <!-- 	</xsl:otherwise> -->
      <!-- </xsl:choose> -->
    </xsl:for-each>
  </xsl:template>

</xsl:stylesheet>
