DEMO_XML = """
<bfaxml xmlns:py="http://purl.org/kid/ns#">
    <config>
            <user access="admin"/>

        <user realname="Team Joe Bob"
              signedcontract="true"
              startingbudget="60000"
              />
        <narrative enabled="True"/>
        <information>
            <info type="doc" name="policeReport" />
        </information>
    </config>
    <testdata>
        <test x="0" y="0" n="8" />
        <test x="0" y="0" n="9" z="10" />
        <test x="6" y="6" n="8" paramstring="blurdy blurd" />
        <test x="0" y="2" n="8" />
        <test x="1" y="4" n="8" />
    </testdata>
    <budget>
        <i a="1500" t="2004/08/30/23/11" d="excavation at 0,0" />
        <i a="1500" t="2004/08/30/23/12" d="excavation at 0,2" />
        <i a="200" t="2004/08/30/23/14" d="sgsa at 0,0" />
        <i a="200" t="2004/08/30/23/15" d="sgsa at 1,4" />
        <i a="1" t="2004/08/31/23/15" d="Questioned Al Milankovitch" />
    </budget>
</bfaxml>
"""


BROWNFIELD_XML = """
<bfaxml xmlns:py="http://purl.org/kid/ns#">
  <config>
    <user realname="${record.name}"
      signedcontract="true"
      startingbudget="${int(record.course.startingBudget)}"
      py:attrs="{'access':record.access}"
      />
    <narrative enabled="${record.course.enableNarrative}" />
    <information>
      <info py:for="i in record.info" type="${i.infoType}"
      name="${i.internalName}"/>
    </information>
  </config>
  <testdata>
    <test py:for="t in record.tests"
      py:attrs="{'paramstring':t.paramString,'z':t.z}"
      x="${t.x}"
      y="${t.y}"
      n="${t.testNumber}" />
  </testdata>
  <budget>
    <i py:for="t in record.history"
       a="${int(t.cost or 0)}"
       t="${t.date and t.date.strftime('%Y/%m/%d/%H/%M')}"
       d="${t.description}" />
  </budget>
</bfaxml>
 """


INITIAL_XML = """<bfaxml>
    <config>
    <user signedcontract="true"
    startingbudget="0" access="professor" realname="Brownfield Demo Team">
    </user>
    <narrative enabled="True"></narrative>
    <information>
    </information>
    </config>
    <testdata>
    </testdata>
    <budget>
    </budget>
    </bfaxml>"""

INFO_TEST = """
        <information>
            <info type="doc" name="policeReport" />
        </information>
"""


TEAM_HISTORY = """
<bfaxml>
  <config>
    <user signedcontract="true" startingbudget="65000" realname="Company 1">
    </user>
    <narrative enabled="True"></narrative>
    <information>
    </information>
  </config>
  <testdata>
  </testdata>
  <budget>
  </budget>
</bfaxml>
"""

TEAM_HISTORY_XML = """
<bfaxml>
  <config>
    <user signedcontract="true" startingbudget="65000" realname="Company 2">
    </user>
    <narrative enabled="True"></narrative>
    <information>
      <info type="recon"></info><info type="doc" name="recon"></info>
    </information>
  </config>
  <testdata>
  </testdata>
  <budget>
    <i a="100" t="2014/10/24/13/06" d="Performed visual reconnaissance.">
    </i><i a="0" t="2014/10/24/13/06" d="Received Visual reconnaissance."></i>
  </budget>
</bfaxml>
"""
