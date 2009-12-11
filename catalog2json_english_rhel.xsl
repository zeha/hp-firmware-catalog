<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<!--
	This XSL transforms catalog.xml into JSON format, and prefilters on the 
	following conditions:
		* Only RHEL5 32-bit & 64-bit is considered
		* Only English (US) is considered
		* An sw_key must be present
-->
<xsl:output method="text"/>
<xsl:template match="/">/* time_stamp: <xsl:value-of select="catalog/@time_stamp"/> */
[
<xsl:for-each select="catalog/cpq_package">
	<xsl:sort select="translate(sw_keys//sw_key/@name, '&#34;', '')" order="ascending"/>
	<xsl:sort select="release_date/@year" order="ascending" data-type="number" />
	<xsl:sort select="release_date/@month" order="ascending" data-type="number" />
	<xsl:sort select="release_date/@day" order="ascending" data-type="number" />
	<!-- Operating System Keys:
		1145 = RHEL5 32-bit
		1147 = RHEL5 64-bit
	 -->
	<xsl:if test="operating_systems/operating_system/@key = '1145' or 
                    operating_systems/operating_system/@key = '1147' 
		">
		<xsl:if test="contains(languages/languages_xlate[@lang='en'],'English (US)')">
			<xsl:if test="sw_keys//sw_key/@name">
				<xsl:call-template name="print_package"/>
			</xsl:if>
		</xsl:if>
	</xsl:if>
    </xsl:for-each>
]
</xsl:template>
<xsl:template name="print_package">{
	sw_keys: "<xsl:value-of select="translate(sw_keys//sw_key/@name, '&#34;', '')"/>",
	reldate: "<xsl:value-of select="format-number(release_date/@year,'####')" />/<xsl:value-of select="format-number(release_date/@month,'00')" />/<xsl:value-of select="format-number(release_date/@day,'00')" />",
	version: "<xsl:value-of select="version/@value"/>",
	name: "<xsl:value-of select="name/name_xlate[@lang='en']" />",
	filename: "<xsl:value-of select="filename"/>",
	url: "<xsl:value-of select="catalog_entry_path"/>",
},
</xsl:template>
</xsl:stylesheet>
