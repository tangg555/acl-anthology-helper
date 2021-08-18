"""
@Author: Travis Tang
@Date: 2021.8.17
@Desc:

from acl.conference import Conference

Conference.ACL(2018).retrieve("P18-5").to_dataframe().to_csv("acl2018.csv", index=False)
"""

from modules import Retriever
from modules.constants import ConfConsts

acl = Retriever.acl(2021, ConfConsts.LONG)
print(acl)
