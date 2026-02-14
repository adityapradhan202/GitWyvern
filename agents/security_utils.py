# Coding for invoking bandit security tests
import subprocess
from typing import List, Dict

class SecurityUtils:
    
    @staticmethod
    def bandit_scan(path:str) -> str:
        """Scans file using bandit"""
        cout = subprocess.run(['bandit', path], text=True, capture_output=True)
        return cout.stdout
    
    @staticmethod
    def vulnerability_count(bandit_cout:str) -> List[int]:
        """Takes in bandit's console output as an argument and returns a list of vulnerability count by severity and by confidence."""

        run_metrics = bandit_cout.split("Run metrics:")[1]
        numbers = run_metrics.split("\n")
        numbers = [n.replace("\t", "") for n in numbers]
        numbers = numbers[2:-2]
        numbers.remove('Total issues (by confidence):')
        numbers = [int(n.split(" ")[1]) for n in numbers]
        return numbers
    
    @staticmethod
    def vulnerability_count_map(bandit_cout:str) -> Dict[str, Dict[str, int]]:
        """Returns a dictionary for vulnaribility count. Takes in bandit's console output as argument."""

        vc_map = {}
        vc = SecurityUtils.vulnerability_count(bandit_cout)
        vc_map['severity'] = {"undefined":vc[0], "low":vc[1], "mid":vc[2], "high":vc[3]}
        vc_map['confidence'] = {"undefined":vc[4], "low":vc[5], "mid":vc[6], "high":vc[7]}

        return vc_map
   
    @staticmethod
    def safety_check(bandit_cout:str) -> str:
        """Checks safety of a file. Returns 'safe' if the file is completely safe, otherwise 'unsafe'"""
        vul_cnt = SecurityUtils.vulnerability_count(bandit_cout)
        total_vul = sum(vul_cnt)
        if total_vul == 0:
            return "safe"
        
        return "unsafe"

    # Use this only when the file has vulnerabilities
    @staticmethod
    def vulnerabilities(bandit_cout:str) -> List[str]:
        """Extracts the issues from bandit's report and returns a list.
        Before using this function check if the file is unsafe or safe using 'safety_check' function.
        """

        vuls = bandit_cout.split("Run metrics:")[0]
        vuls = vuls.replace("\t", "").replace("\n", "").replace("-", "")
        vuls_list = vuls.split(">>")
        vuls_list = [vul for vul in vuls_list if "Issue:" in vul]
        
        return vuls_list