<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl">
 
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
 
  <xsl:template match="/class">
    <table border="0" cellborder="1" cellspacing="0" 
	   cellpadding = "4"
	   bgcolor = "lightgray">
      <xsl:attribute name="href">
	<xsl:value-of select="@location" />
      </xsl:attribute>
      <tr><td><xsl:if test="./modifiers != ''">
	<font face="Arial" point-size = "12"><xsl:value-of select="modifiers"/></font><br/>
      </xsl:if>
      <xsl:if test="./@detalization-level > 3">
      [<xsl:value-of select="@package"/>]</xsl:if>
      <xsl:choose>
	<xsl:when test="@interface = 'yes' ">
	  <i><b><xsl:value-of select="text()"/></b></i>
	</xsl:when>
	<xsl:otherwise>
	  <b><xsl:value-of select="text()"/></b>
	</xsl:otherwise>
      </xsl:choose>
      </td></tr>
      <xsl:if test="./@detalization-level > 1">
	<xsl:apply-templates select="attributes"/>
	<xsl:apply-templates select="methods"/>
      </xsl:if>
    </table>
  </xsl:template>


  <xsl:template match="class/attributes/attribute/type">
    <xsl:comment>
      </xsl:comment>:<xsl:value-of select="text()"/> <xsl:value-of select="@multiplicity"/>
      <xsl:if test="../../../@detalization-level > 2">
	<xsl:value-of select="@properties"/>
      </xsl:if>
  </xsl:template>

  <xsl:template match="class/methods/method/type">
      <xsl:if test="text() != '' ">
	<xsl:comment>
	  </xsl:comment>:<xsl:value-of select="text()"/> <xsl:value-of select="@multiplicity"/>
      </xsl:if>
  </xsl:template>

  <xsl:template match="class/attributes">
    <tr><td align="left"><xsl:comment><font point-size = "10">
      </font> </xsl:comment><xsl:apply-templates select="attribute"/>
    </td></tr>
  </xsl:template>
  <xsl:template match="class/attributes[not(attribute)]">
    <tr><td>
      &#x200B;
    </td></tr>
  </xsl:template>

  <xsl:template match="class/attributes/attribute">
    <xsl:value-of select="@visibility"/><xsl:value-of select="text()"/><xsl:apply-templates select="type"/>
    <br align="left"/>
  </xsl:template>


  <xsl:template match="class/methods">
    <tr><td align="left">
      <xsl:apply-templates select="method"/>
    </td></tr>
  </xsl:template>
  <xsl:template match="class/methods[not(method)]">
    <tr><td>
      &#x200B;
    </td></tr>
  </xsl:template>

  <xsl:template name="class-method.basic">
    <xsl:value-of select="@visibility"/><xsl:comment>
    </xsl:comment><xsl:call-template name="class-method.name"/>()<xsl:comment>
    </xsl:comment><xsl:if test="../../@detalization-level > 2">
    <xsl:apply-templates select="type"/>
    <xsl:value-of select="@properties"/>
  </xsl:if>
  </xsl:template>

  <xsl:template name="class-method.name">
    <xsl:choose>
      <xsl:when test="./@abstract = 'yes' ">
	<i><xsl:value-of select="text()"/></i>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="text()"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="class/methods/method">
    <xsl:call-template name="class-method.basic"/>
    <br align="left"/>
  </xsl:template>

</xsl:stylesheet>
