<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl"
    xml:space="preserve">

  <xsl:template name="show-visibility-img">
    <xsl:choose>
      <xsl:when test="./@visibility = '-'">
	<span title='private'><img src="css/icons/privattr.gif" alt="- " /></span>
      </xsl:when>
      <xsl:when test="./@visibility = '+'">
	<span title='public'><img src="css/icons/privattr.gif" alt="+ " /></span>
      </xsl:when>
      <xsl:when test="./@visibility = '#'">
	<span title='protected'><img src="css/icons/privattr.gif" alt="# " /></span>
      </xsl:when>

      <xsl:when test="./@visibility = '- '">
	<span title='private'><img src="css/icons/privoper.gif" alt="- " /></span>
      </xsl:when>
      <xsl:when test="./@visibility = '+ '">
	<span title='public'><img src="css/icons/publoper.gif" alt="+ " /></span>
      </xsl:when>
      <xsl:when test="./@visibility = '# '">
	<span title='protected'><img src="css/icons/protoper.gif" alt="# " /></span>
      </xsl:when>

      <xsl:when test="./@visibility = '-/'">
	<span title='private virtual'><img src="css/icons/virtprivoper.gif" alt="-/" /></span>
      </xsl:when>
      <xsl:when test="./@visibility = '+/'">
	<span title='public virtual'><img src="css/icons/virtpubloper.gif" alt="+/" /></span>
      </xsl:when>
      <xsl:when test="./@visibility = '#/'">
	<span title='protected virtual'><img src="css/icons/virtprotoper.gif" alt="#/" /></span>
      </xsl:when>

      <xsl:otherwise>
	<xsl:value-of select="./@visibility"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- See for more http://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs -->
  <!-- 1F31F - star -->
  <!-- 1F446 - pointer -->
  <xsl:template name="show-visibility-unicode">
    <xsl:choose>
      <xsl:when test="./@visibility = '-'">
	<span title='private'><font color='red'>&#x25AB;</font></span>
	<!-- <span title='private'><font color='red'>&#x1F512;</font></span> -->
      </xsl:when>
      <xsl:when test="./@visibility = '+'">
	<span title='public'><font color='green'>&#x26AC;</font></span>
	<!-- <span title='public'><font color='green'>&#x1F511;</font></span> -->
      </xsl:when>
      <xsl:when test="./@visibility = '#'">
	<span title='protected'><font color='yellow'>&#x22C4;</font></span>
	<!-- <span title='protected'><font color='yellow'>&#x1F510;</font></span> -->
      </xsl:when>

      <xsl:when test="./@visibility = '- '">
	<span title='private'><font color='red'>&#x25A0;</font></span>
	<!-- <span title='private'><font color='red'>&#x1F512;</font></span> -->
      </xsl:when>
      <xsl:when test="./@visibility = '+ '">
	<span title='public'><font color='green'>&#x26AB;</font></span>
	<!-- <span title='public'><font color='green'>&#x1F511;</font></span> -->
      </xsl:when>
      <xsl:when test="./@visibility = '# '">
	<span title='protected'><font color='yellow'>&#x2B29;</font></span>
	<!-- <span title='protected'><font color='yellow'>&#x1F510;</font></span> -->
      </xsl:when>

      <xsl:when test="./@visibility = '-/'">
	<span title='private virtual'><font color='red'>&#x2699;</font></span>
      </xsl:when>
      <xsl:when test="./@visibility = '+/'">
	<span title='public virtual'><font color='green'>&#x2699;</font></span>
      </xsl:when>
      <xsl:when test="./@visibility = '#/'">
	<span title='protected virtual'><font color='yellow'>&#x2699;</font></span>
      </xsl:when>

      <xsl:otherwise>
	<xsl:value-of select="./@visibility"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="show-visibility-plain">
    <xsl:value-of select="./@visibility"/>
  </xsl:template>

</xsl:stylesheet>
