#!/usr/bin/env python


class NessusReportItem(object):
    """This class represent a ReportItem in the nessus xml"""
    def __init__(self, vuln_info={}):
        """Constructor of Vulnerability
           :param vuln_info: dict of vulnerabities as generated by
           NessusParser.parse_reportitem
        """
        _minimal_attr = set(['port', 'svc_name', 'protocol', 'severity'])

        _vuln_info_attr = set(vuln_info.keys())
        _missing_attr = _minimal_attr.difference(_vuln_info_attr)

        if len(_missing_attr) == 0:
            self.__vuln_info = vuln_info
        else:
            raise Exception("Not all the attributes to create a decent "
                            "NessusVuln object are available. "
                            "Missing: ".format(" ".join(_missing_attr)))

    def __repr__(self):
        return "{0}:{1} {2}".format(self.plugin_id,
                                    self.plugin_name,
                                    self.severity
                                    )

    def __hash__(self):
        return(hash(self.plugin_id))

    @property
    def port(self):
        """
        Get the port where the vuln is detected, 0 if not network detected
        :return str
        """
        return self.__vuln_info['port']

    @property
    def service(self):
        """
        Get the service name if known
        :return str
        """
        return self.__vuln_info['svc_name']

    @property
    def protocol(self):
        """
        Get the protocol
        :return str
        """
        return self.__vuln_info['protocol']

    @property
    def severity(self):
        """
        Get Severity level, It corresponds with a
        "0" as an open port,
        "1" as a low or informational
        "2" as a medium or warning and
        "3" as a high or hole
        return str
        """
        return self.__vuln_info['severity']

    @property
    def plugin_id(self):
        """
        Get the plugin id
        :return str
        """
        return self.__vuln_info['pluginID']

    @property
    def plugin_name(self):
        """
        Get the plugin Name
        :return str
        """
        return self.__vuln_info['plugin_name']

    @property
    def plugin_family(self):
        """
        Get the test Family
        :return str
        """
        return self.__vuln_info['pluginFamily']

    @property
    def get_vuln_info(self):
        """
        Get a dict of the whole vulnerability
        :return dict
        """
        return self.__vuln_info

    @property
    def get_vuln_risk(self):
        """
        Get a dict of the risk
        should return a dict with key of the internal dict that match patterns:
        'risk_factor' or 'cvss_*'
        :return dict
        """
        # syntax allowed from 2.7>= or 3 damnit!
        # risk = {k:v for (k,v) in __vuln_info.items() if k.startswith("cvss_")
        # or k.startswith("risk_factor")}
        risk = dict(
            (k, v) for (k, v) in self.__vuln_info.items()
            if k.startswith("cvss_") or k.startswith("risk_factor")
            )
        return risk

    @property
    def get_vuln_plugin(self):
        """
        Get a dict of plugin
        :return dict
        """
        plugindetail = dict(
            (k, v) for (k, v) in self.__vuln_info.items()
            if k.startswith("plugin") or k.startswith("script_version")
            )
        return plugindetail

    @property
    def get_vuln_xref(self):
        """
        Get a dict of xref
        expected :
        { 'cve': [], 'cwe': [], 'bid': [], 'osvdb': [],
          'iava': [], 'iavb': [], 'cert': [], 'xref': []
        }
        :return dict
        """
        need = ['cve', 'bid', 'osvdb', 'iava', 'iavb', 'xref']
        xref = dict(
            (k, v) for (k, v) in self.__vuln_info.items()
            if k in need
            )
        return xref

    @property
    def synopsis(self):
        """
        Get the sypnosis of the vuln
        :return str
        """
        return self.__vuln_info['synopsis']

    @property
    def description(self):
        """
        Get description
        :return str
        """
        return self.__vuln_info['description']

    @property
    def solution(self):
        """
        Get the sulution provide by nessus
        :return str
        """
        return self.__vuln_info['solution']
