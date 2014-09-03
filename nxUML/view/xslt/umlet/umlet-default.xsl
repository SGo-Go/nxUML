<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl">
  
  <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
  
  <xsl:template match="/class">
    <!-- <xsl:text>&lt;?xml version="1.0" encoding="UTF-8" standalone="no"?&gt;</xsl:text> -->
    <diagram program="umlet" version="12.2">
      <zoom_level>10</zoom_level>
      <xsl:call-template name="show-body-class-default"/>
    </diagram>
  </xsl:template>
  <xsl:strip-space elements="operation attribute operations attributes panel_attributes"/> 

  <xsl:template match="/interface">
  </xsl:template>

  <xsl:template match="/package">
  </xsl:template>

  <xsl:template name="show-coordinates">
    <coordinates>
      <x>10</x>
      <y>10</y>
      <w>300</w>
      <h>1000</h>
    </coordinates>
  </xsl:template>

  <xsl:template match="@* | node()">
    <xsl:copy>
      <xsl:apply-templates select="@* | node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="text()">
    <xsl:value-of select="normalize-space()"/>
  </xsl:template>

  <!-- <xsl:include href = "../nxUML/view/xslt/umlet/umlet-class.xsl"/> -->
  <xsl:include href = "../umlet/umlet-class.xsl"/>

  <!-- ********************************************************* -->
  <!-- Customize HTML by choosing templates from the common list -->
  <!-- ********************************************************* -->
  <!-- <xsl:include href = "../nxUML/view/xslt/common/feature.xsl"/> -->
  <xsl:include href = "../common/feature.xsl"/>
  <xsl:template match="//attributes/attribute">
    <!-- <xsl:value-of select="normalize-space()"/> -->
    <xsl:call-template name="show-attribute-signature-short"/>&#160;
  </xsl:template>

  <xsl:template match="//operations/operation">
    <!-- <xsl:value-of select="normalize-space()"/> -->
    <xsl:call-template name="show-operation-signature-short"/>&#160;
  </xsl:template>

  <!-- <xsl:include href = "../nxUML/view/xslt/common/name.xsl"/> -->
  <xsl:include href = "../common/name.xsl"/>

  <xsl:template name="show-name">
    <xsl:call-template name="show-name-plain"/>
  </xsl:template>
  <xsl:template name="show-reference">
    <xsl:call-template name="show-name-plain"/>
  </xsl:template>

  <!-- <xsl:include href = "../nxUML/view/xslt/common/visibility.xsl"/> -->
  <xsl:include href = "../common/visibility.xsl"/>
  <xsl:template name="show-visibility">
    <xsl:call-template name="show-visibility-plain"/>
  </xsl:template>
  
  <!-- <xsl:include href = "../nxUML/view/xslt/common/multiplicity.xsl"/> -->
  <xsl:include href = "../common/multiplicity.xsl"/>
  <xsl:template name="show-multiplicities">
    <xsl:call-template name="show-multiplicity-plain"/>
  </xsl:template>

  <!-- <xsl:include href = "../nxUML/view/xslt/common/property.xsl"/> -->
  <xsl:include href = "../common/property.xsl"/>
  <xsl:template name="show-properties">
    <xsl:value-of select="normalize-space()"/>
    <xsl:call-template name="show-properties-plain"/>
  </xsl:template>

</xsl:stylesheet>
