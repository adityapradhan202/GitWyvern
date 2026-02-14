from agents import SecurityUtils
from agents import AgentUtils

def test_security_utils(test_dir:str) -> None:
    """Imports and checks if all the security utils are working fine!"""

    print(f"\n---- Testing security utils on directory - {test_dir} ----\n")
    # test_dir is the testing directory/folder
    # This folder must be present at the root directory level
    dirs = AgentUtils.code_files(test_dir)
    n_test_cases = len(dirs)

    # Succesful safety checks execution
    n_safety_checks = 0
    total_unsafe_files = 0
    n_valid_vc = 0
    n_valid_vc_map = 0
    n_vuls = 0 # Succesfully listing vulnerabilities

    for dir in dirs:
        print(f"Performing tests on - {dir}")
        bandit_cout = SecurityUtils.bandit_scan(dir)
        scheck = SecurityUtils.safety_check(bandit_cout)
        if scheck == "safe":
            n_safety_checks += 1
            try:
                vc = SecurityUtils.vulnerability_count(bandit_cout)
                if sum(vc) >= 0:
                    n_valid_vc += 1
            except:
                print(f"Vulnarability count faild on - {dir}")
            try:
                vc_map = SecurityUtils.vulnerability_count_map(bandit_cout)
                if vc_map:
                    n_valid_vc_map += 1
            except:
                print(f"Vunarability count map failed on - {dir}")

        elif scheck == "unsafe":
            n_safety_checks += 1
            total_unsafe_files += 1
            # We use SecuritUtils.vulnerabilities only when the file is unsafe
            try:
                vuls = SecurityUtils.vulnerabilities(bandit_cout)
                if vuls:
                    n_vuls += 1
            except:
                print(f"Listing vulnarabilities failed on  - {dir}")

    print("\nSecurity Utils test results:\n")
    print(f"Safety check util [Passed/Total] - {n_safety_checks}/{n_test_cases}")
    print(f"Vunlarability count [Passed/Total] - {n_valid_vc}/{n_safety_checks-total_unsafe_files}")
    print(f"Vulnarability count map [Passed/Total] - {n_valid_vc_map}/{n_safety_checks-total_unsafe_files}")
    print(f"Listing vulnarabilities descriptions [Passed/Total] - {n_vuls}/{total_unsafe_files}")

    

if __name__ ==  "__main__":
    # Testing the utils folder of this project 
    test_security_utils(test_dir='./utils')
    print()
    test_security_utils(test_dir='./agents')
    