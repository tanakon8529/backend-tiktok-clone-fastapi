from typing import List
from urllib import response, request, parse, error
from urllib.request import urlopen
from urllib.error import URLError
import json

from app.settings.configs import K2_URL_PREFIX
from loguru import logger

from app.core.db_model import lt_m_doc_type_Base, lt_nonpo_info_Base, lt_m_user_role_Base, lt_m_role_Base, lt_legal_doc_info_Base
from app.apis.documents.model.model_non_po_contract import lt_nonpo_info_ModelBase
from app.apis.documents.model.model_legal_doc import lt_legal_doc_info_ModelBase
from app.apis.worklist import model_worklist
from app.apis.doc_type.model_doc_type import DocTypeModelBase


def get_users_by_role_name(role_name, db_session):
    result = db_session.query(lt_m_user_role_Base).join(lt_m_role_Base,lt_m_user_role_Base.role_id==lt_m_role_Base.role_id, isouter=True).filter(lt_m_role_Base.role_name==role_name).all()
    return result

def get_users_by_role_id(role_id, db_session):
    result = db_session.query(lt_m_user_role_Base).filter(lt_m_user_role_Base.role_id==role_id).all()
    return result

def get_lt_non_po_info_by_doc_id(doc_id, db_session):
    query_session_lt_nonpo_info = db_session.query(lt_nonpo_info_Base).filter(lt_nonpo_info_Base.rq_info_id==doc_id)
    result_lt_nonpo_info = []
    for i in query_session_lt_nonpo_info:
        x = lt_nonpo_info_ModelBase(**i.__dict__)
        result_lt_nonpo_info.append(x)

    if result_lt_nonpo_info == []:
        return query_session_lt_nonpo_info, None

    result_query_lt_nonpo_info = result_lt_nonpo_info[0]
    return query_session_lt_nonpo_info, result_query_lt_nonpo_info

def get_lt_legal_doc_by_doc_id(doc_id, db_session):
    query_session_lt_nonpo_info = db_session.query(lt_legal_doc_info_Base).filter(lt_legal_doc_info_Base.rq_info_id==doc_id)
    result_lt_nonpo_info = []
    for i in query_session_lt_nonpo_info:
        x = lt_legal_doc_info_ModelBase(**i.__dict__)
        result_lt_nonpo_info.append(x)

    if result_lt_nonpo_info == []:
        return query_session_lt_nonpo_info, None

    result_query_lt_nonpo_info = result_lt_nonpo_info[0]
    return query_session_lt_nonpo_info, result_query_lt_nonpo_info    

def create_workflow(workflow_dict):
    
    try:
        url = K2_URL_PREFIX+"/submit"
        logger.debug(f"Starting create workflow K2 for {workflow_dict['rq_doc_num']} url:{url}")

        req = request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header("Accept", "application/json")
        jsondata = json.dumps(workflow_dict)
        logger.debug(f"k2_body_{workflow_dict['rq_doc_num']}")
        logger.debug(jsondata)
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        response = request.urlopen(req, jsondataasbytes)
        result = json.loads(response.read())
        logger.debug(f"Submit K2 workflow for doc_id:{workflow_dict['id']} successfully ... ")
    except Exception as e:
        logger.error(e)
        result = {"Response":
                    {"error_code": "02","msg": "K2 API service doesn't response or some field mismatch"}
        }

    return result

def create_workflow_nonpo(doc_dict, session):
    logger.debug("Start create workflow non-po ...")
    logger.debug(f"Preparing body for K2 {doc_dict['rq_doc_num']}")

    workflow_dict = dict()

    detail_result = get_workflow_detail(doc_dict, session)
    if detail_result == None:
        logger.debug(f"doc_id:{doc_dict['rq_info_id']} workflow does NOT EXIST on K2 ... moving on to create doc")
    else:
        logger.debug(f"K2 workflow alredy exists for rq_info_id:{doc_dict['rq_info_id']} with response below:")
        logger.debug(detail_result)
        return {"Response":{
                            "error_code": "02",
                            "msg": f"K2 workflow alredy exists for rq_info_id:{doc_dict['rq_info_id']}"
                            }
        } 


    workflow_dict.update({
        ########## dummy send stampDutyType (remove when production) ##########
        # "stampDutyType": 0,
        ################ fixed value by K2 ################
        "documentUrl": "None",
        "comment": "",
        "specialProjectId": 0,
        "goa": "LegalTicket",
        ################ End fixed value by K2 ################
        "documentNumber": doc_dict["rq_doc_num"],
        "id": doc_dict["rq_info_id"],
        "title": doc_dict["rq_title"],
        "totalAmount": doc_dict["am_total_amt"],
        "creatorUser": doc_dict["rq_creator_name"],
        "requesterUser": doc_dict["rq_requester_name"],
        "documentDate": str(doc_dict["rq_create_date"]),
        "docTypeId": doc_dict["doc_type_id"],
        "purposeId": 9999,
        "companyCode": doc_dict["comp_code"],
        "vendor": doc_dict["vendor_code"],
        "rq_doc_num": doc_dict["rq_doc_num"]
    })

    ########### Adding Admin Legal list #########
    query_users = get_users_by_role_name("Admin Legal", session)
    user_list = list()
    for user in query_users:
        user_list.append({
            "userName": user.user_name,
            "email": user.user_email
            })

    workflow_dict.update({
        "legalAdmins": user_list
    })

    ########### Adding Legal Approval list #########
    query_users = get_users_by_role_name("Legal Approval", session)
    user_list = list()
    for user in query_users:
        user_list.append({
            "userName": user.user_name,
            "email": user.user_email
            })

    workflow_dict.update({
        "legalApprovals": user_list
    })

    return create_workflow(workflow_dict)


def create_workflow_legaldoc(doc_dict, session):
    logger.debug("Starting K2 workflow process .... ")
    logger.debug(f"Preparing legal doc for create_k2 workflow {doc_dict['rq_doc_num']}")

    workflow_dict = dict()

    detail_result = get_workflow_detail(doc_dict, session)
    if detail_result == None:
        logger.debug(f"doc_id:{doc_dict['rq_info_id']} workflow does NOT EXIST on K2 ... moving on to create doc")
    else:
        logger.debug(f"K2 workflow alredy exists for rq_info_id:{doc_dict['rq_info_id']} with response below:")
        logger.debug(detail_result)
        return {"Response":{
                            "error_code": "02",
                            "msg": f"K2 workflow alredy exists for rq_info_id:{doc_dict['rq_info_id']}"
                            }
        } 

    workflow_dict.update({
        ################ fixed value by K2 ################4
        "documentUrl": "None",
        "comment": "",
        "specialProjectId": 0,
        "goa": "LegalTicket",
        ################ End fixed value by K2 ################
        "documentNumber": doc_dict["rq_doc_num"],
        "id": doc_dict["rq_info_id"],
        "title": doc_dict["rq_title"],
        "creatorUser": doc_dict["rq_creator_name"],
        "requesterUser": doc_dict["rq_requester_name"],
        "documentDate": str(doc_dict["rq_create_date"]),
        "docTypeId": doc_dict["doc_type_id"],
        "purposeId": doc_dict["purpose_id"],
        "companyCode": doc_dict["comp_code"],
        "rq_doc_num": doc_dict["rq_doc_num"],
        "certified": doc_dict["certified"],
        "totalAmount": 0
    })

    ########### Adding Admin Legal list #########
    query_users = get_users_by_role_name("Admin Legal", session)
    user_list = list()
    for user in query_users:
        user_list.append({
            "userName": user.user_name,
            "email": user.user_email
            })

    workflow_dict.update({
        "legalAdmins": user_list
    })

    ########### Adding Legal Approval list #########
    query_users = get_users_by_role_name("Legal Approval", session)
    user_list = list()
    for user in query_users:
        user_list.append({
            "userName": user.user_name,
            "email": user.user_email
            })

    workflow_dict.update({
        "legalApprovals": user_list
    })

    return create_workflow(workflow_dict)

def create_workflow_legaldocservice(doc_dict, session):
    logger.debug("Starting K2 workflow process .... ")
    logger.debug(f"Preparing legal doc and service for create_k2 workflow {doc_dict['rq_doc_num']}")

    workflow_dict = dict()

    detail_result = get_workflow_detail(doc_dict, session)
    if detail_result == None:
        logger.debug(f"doc_id:{doc_dict['rq_info_id']} workflow does NOT EXIST on K2 ... moving on to create doc")
    else:
        logger.debug(f"K2 workflow alredy exists for rq_info_id:{doc_dict['rq_info_id']} with response below:")
        logger.debug(detail_result)
        return {"Response":{
                            "error_code": "02",
                            "msg": f"K2 workflow alredy exists for rq_info_id:{doc_dict['rq_info_id']}"
                            }
        }
    
    # gov_auth = list()
    # gov_auth.append(doc_dict["thai_Industrial"])
    # gov_auth.append(doc_dict["bk_metropolitan"])
    # gov_auth.append(doc_dict["land_office"])
    # gov_auth.append(doc_dict["dept_biz_develop"])
    # gov_auth.append(doc_dict["dept_Intellectual"])
    # gov_auth.append(doc_dict["nation_broadcast"])
    # gov_auth.append(doc_dict["electricity"])
    # gov_auth.append(doc_dict["waterwork"])
    # gov_auth.append(doc_dict["revenue_dept"])
    # gov_auth.append(doc_dict["excise_dept"])
    # gov_auth.append(doc_dict["food_drug"])
    # gov_auth.append(doc_dict["other"])
    # gov_auth.append(doc_dict["other_desc"])

    gov_tuple = (
        "thai_Industrial",
        "bk_metropolitan",
        "land_office",
        "dept_biz_develop",
        "dept_Intellectual",
        "nation_broadcast",
        "electricity",
        "waterwork",
        "revenue_dept",
        "excise_dept",
        "food_drug",
        "other",
        "other_desc"
        )
    gov_auth = str

    logger.debug(f"selected gov_auth:")
    for item in gov_tuple:
        if doc_dict[item]:
            logger.debug(f"{doc_dict[item]}")
            gov_auth += doc_dict[item]


    workflow_dict.update({
        ################ fixed value by K2 ################4
        "documentUrl": "None",
        "comment": "",
        "specialProjectId": 0,
        "goa": "LegalTicket",
        ################ End fixed value by K2 ################
        "documentNumber": doc_dict["rq_doc_num"],
        "id": doc_dict["rq_info_id"],
        "title": doc_dict["rq_title"],
        "creatorUser": doc_dict["rq_creator_name"],
        "requesterUser": doc_dict["rq_requester_name"],
        "documentDate": str(doc_dict["rq_create_date"]),
        "docTypeId": doc_dict["doc_type_id"],
        "companyCode": doc_dict["comp_code"],
        "rq_doc_num": doc_dict["rq_doc_num"],
        "gov_auth": gov_auth,
        "totalAmount": 0
    })

    ########### Adding Admin Legal list #########
    query_users = get_users_by_role_name("Admin Legal", session)
    user_list = list()
    for user in query_users:
        user_list.append({
            "userName": user.user_name,
            "email": user.user_email
            })

    workflow_dict.update({
        "legalAdmins": user_list
    })

    ########### Adding Legal Approval list #########
    query_users = get_users_by_role_name("Legal Approval", session)
    user_list = list()
    for user in query_users:
        user_list.append({
            "userName": user.user_name,
            "email": user.user_email
            })

    workflow_dict.update({
        "legalApprovals": user_list
    })

    return create_workflow(workflow_dict)    

def get_workflow_detail_by_doc_id(id:int, doc_type_id:int, username:str, session):
    logger.debug(f"Getting doc detail by doc_id:{id} doc_type_id:{doc_type_id} ... ")
    try:
        doc = None
        query_session = None

        if doc_type_id == 1:
            query_session, doc = get_lt_non_po_info_by_doc_id(id, session)
        elif doc_type_id == 2:
            query_session, doc = get_lt_legal_doc_by_doc_id(id, session)
        
        if doc == None:
            return None
        
        doc_dict = doc.dict()

        if "purpose_id" in doc_dict:
            purpose_id = doc_dict['purpose_id']
        else:
            purpose_id = 9999
        
        #### K2 get detail URL pattern
        ###  https://ostest.dtgsiam.com/GOAService/api/v1/legalTicket/124/siriporn_ou/1?docTypeId=1&purposeId=999

        url = f"{K2_URL_PREFIX}/{id}/{username}/{doc_dict['doc_type_id']}?docTypeId={doc_dict['doc_type_id']}&purposeId={purpose_id}"
        logger.debug(url)
        response = urlopen(url)
        result_json = json.loads(response.read())

        data_json = dict()
        data_json.update({
            "workflow_detail":{
                "rq_doc_num": result_json["Response"]["data"]["documentNumber"],
                "doc_id": result_json["Response"]["data"]["documentId"],
                "actions": result_json["Response"]["data"]["actions"],
                "action_logs": result_json["Response"]["data"]["actionLogs"],
                "approver_steps": result_json["Response"]["data"]["approverSteps"]

            }
        })

    except(URLError) as err:
        return {"error_code": "02","msg": f"doc_id:{doc_dict['rq_info_id']} workflow already EXIST on K2"}

    return data_json

def get_workflow_detail(doc_dict, session):
    try:

        if "purpose_id" in doc_dict:
            purpose_id = doc_dict['purpose_id']
        else:
            purpose_id = 9999
        
        #### K2 get detail URL pattern
        ###  https://ostest.dtgsiam.com/GOAService/api/v1/legalTicket/124/siriporn_ou/1?docTypeId=1&purposeId=999

        url = f"{K2_URL_PREFIX}/{doc_dict['rq_info_id']}/{doc_dict['rq_creator_name']}/{doc_dict['doc_type_id']}?docTypeId={doc_dict['doc_type_id']}&purposeId={purpose_id}"
        logger.debug(url)
        response = urlopen(url)
        result_json = json.loads(response.read())
        logger.debug(f"K2 response :")
        logger.debug(result_json)
        
        print(result_json["Response"]["data"]["error"]["isError"])
        if result_json["Response"]["data"]["error"]["isError"] == True:
            return None

        data_json = dict()
        data_json.update({
            "workflow_detail":{
                "doc_id": result_json["Response"]["data"]["documentId"],
                "actions": result_json["Response"]["data"]["actions"],
                "action_logs": result_json["Response"]["data"]["actionLogs"],
                "approver_steps": result_json["Response"]["data"]["approverSteps"]
            }
        })

    except(URLError) as err:
        return None

    return data_json

def get_k2_worklist(username:str):
    try:
        url = f"{K2_URL_PREFIX}/worklist/{username}"
        response = urlopen(url)
        data_json = json.loads(response.read())
    except(URLError) as err:
        return None

    return data_json    

def update_workflow_k2(workflow_dict):
    try:
        logger.debug(workflow_dict)
        # url = K2_URL_PREFIX+"/actionWorkflow"
        url = f"{K2_URL_PREFIX}/actionWorkflow?docTypeId={workflow_dict['doc_type_id']}&purposeId={workflow_dict['purpose_id']}"
        ## https://ostest.dtgsiam.com/GOAService/api/v1/legalTicket/actionWorkflow?docTypeId=2&purposeId=2
        logger.debug(f"k2 url: {url}")

        req = request.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header("Accept", "application/json")
        jsondata = json.dumps(workflow_dict)
        jsondataasbytes = jsondata.encode('utf-8')
        logger.debug(f"K2 workflow: body from API to K2")
        logger.debug(jsondataasbytes)
        req.add_header('Content-Length', len(jsondataasbytes))
        response = request.urlopen(req, jsondataasbytes)
        result = json.loads(response.read())
        logger.debug(f"Action K2 workflow for doc_id:{workflow_dict['documentId']} successfully ... ")
    except error.HTTPError as e:
        logger.error(e)
        body = e.read().decode()
        result = json.loads(body)
    return result

def update_workflow_nonpo(doc_dict, session):
    logger.debug("begin prepare non-po doc for update workflow ...")
    #### prepare Non-PO workflow dict ####
    # doc_dict = doc.dict()

    doc_type_id = 1     # non-po doc_type_id = 1
    workflow_dict = dict()
    action_button = str(doc_dict["action_button"])
    sn = None

    doc_id = doc_dict["rq_info_id"]

    if action_button.lower() == "cancel":
        action_username = doc_dict["action_by_name"]
    else:
        action_username = doc_dict["action_update_by_name"]

    workflow_dict.update({
        #### non-po doc has no purpose_id and purpose_name fields then set it to 9999 ####
        "purpose_id": 9999
    })

    ####### Recall action doesn't need Serial Number to send to K2 ##########
    if action_button.lower() != "recall":
        logger.debug("Update action need Serial Number for K2")
        ######### get sn from K2 Detail API ###########
        url = f"{K2_URL_PREFIX}/{doc_id}/{action_username}/{doc_type_id}?docTypeId={doc_type_id}&purposeId=9999"
        logger.debug(f"getting sn from K2 Detail url:{url}")
        response = urlopen(url)
        result_json = json.loads(response.read())
        sn = result_json["Response"]["data"]["sn"]

        logger.debug(f"sn = {sn}")

        if sn == None:
            result = {
                        "Response":{
                            "error_code": "02","msg": f"No Serial Number in response from K2 for {doc_dict['rq_doc_num']}"
                            }
                    }
            return result
    else:
        logger.debug("Recall action doesn't need Serial Number for K2")

    if doc_dict["req_for_stamp"] != "":
        workflow_dict.update({
            "stampDutyType": doc_dict["req_for_stamp"],
        })
    
    workflow_dict.update({
        "documentId": doc_dict["rq_info_id"],
        "action": action_button,
        "actionByUserName": action_username,
        "actionByFullName": "",
        "comment": doc_dict["comment_detail"],
        "doc_type_id": doc_type_id,
        "sn": sn
    })

    if action_button.lower() != "cancel":

        commitees = list()
        commitees.append({
            "userName":doc_dict["sg_rq_approver"],
            "email": doc_dict["sg_rq_approver_email"]
            })
        commitees.append({
            "userName":doc_dict["sg_acnt"],
            "email": doc_dict["sg_acnt_email"]
            })
        commitees.append({
            "userName":doc_dict["sg_purch"],
            "email": doc_dict["sg_purch_email"]
            })

        authorities = list()
        authorities.append({
            "userName":doc_dict["sg_auth1"],
            "email": doc_dict["sg_auth1_email"]
            })
        authorities.append({
            "userName":doc_dict["sg_auth2"],
            "email": doc_dict["sg_auth2_email"]
            })
        authorities.append({
            "userName":doc_dict["sg_auth3"],
            "email": doc_dict["sg_auth3_email"]
            })   


        logger.debug(f"action_button: {action_button}")
        workflow_dict.update({
            "mainContractUser": doc_dict["sg_main_contact"],
            "committees": commitees,
            "authorities": authorities
        })

        ########### Adding Legal Approval list #########
        query_users = get_users_by_role_name("Legal Approval", session)
        user_list = list()
        for user in query_users:
            user_list.append({
                "userName": user.user_name,
                "email": user.user_email
                })

        workflow_dict.update({
            "legalApprovals": user_list
        })
    else:
        logger.debug(f"action_button: {action_button}")

    return update_workflow_k2(workflow_dict)   

def update_workflow_legaldoc(doc_dict, session):
        
    logger.debug(f"Preparing Legal-Doc for K2 ... ")

    doc_type_id = 2     # legal doc doc_type_ie = 2
    workflow_dict = dict()
    authorities = list()
    action_button = doc_dict["action_button"]
    doc_id = doc_dict["rq_info_id"]
    sn = None

    workflow_dict.update({
        "purpose_id": doc_dict["purpose_id"]
    })
    if(action_button.lower() == "cancel"):
        action_username = doc_dict["action_by_name"]
        logger.debug(f"preparing for cancel:{doc_dict['rq_doc_num']}")
    else:
        action_username = doc_dict["action_update_by_name"]
        authorities.append({
            "userName":doc_dict["sg_auth1"],
            "email": doc_dict["sg_auth1_email"]
            })
        authorities.append({
            "userName":doc_dict["sg_auth2"],
            "email": doc_dict["sg_auth2_email"]
            })
        authorities.append({
            "userName":doc_dict["sg_auth3"],
            "email": doc_dict["sg_auth3_email"]
            })
        workflow_dict.update({
            "certified": doc_dict["certified"],
            "mainContractUser": doc_dict["sg_main_contact"],
            "authorities": authorities
        })

        ########### Adding Legal Approval list #########
        query_users = get_users_by_role_name("Legal Approval", session)
        user_list = list()
        for user in query_users:
            user_list.append({
                "userName": user.user_name,
                "email": user.user_email
                })

        workflow_dict.update({
            "legalApprovals": user_list
        })

    ###### Recall action don't need to send sn to K2 #########
    if action_button.lower() != "recall":
        ######### get sn from K2 API ###########
        url = f"{K2_URL_PREFIX}/{doc_id}/{action_username}/{doc_type_id}?docTypeId={doc_type_id}&purposeId={doc_dict['purpose_id']}"
        logger.debug(f"getting sn from K2 url:{url}")

        response = urlopen(url)
        result_json = json.loads(response.read())
        sn = result_json["Response"]["data"]["sn"]
        logger.debug(f"sn = {sn}")
    
        if sn == None:
            result = {
                        "Response":{
                            "error_code": "02","msg": f"No Serial Number in response from K2 for {doc_dict['rq_doc_num']}"
                            }
                    }
            return result
    else:
        logger.debug("Recall action doesn't need Serial Number for K2")

    workflow_dict.update({
        "documentId": doc_dict["rq_info_id"],
        "action": action_button,
        "actionByUserName": action_username,
        "actionByFullName": "",
        "comment": doc_dict["comment_detail"],
        "doc_type_id": doc_type_id,
        "sn": sn,
        "totalAmount":0
    })

    return update_workflow_k2(workflow_dict)       

def update_workflow_legaldocservice(doc_dict, session):
    return None

def get_doctype_by_id(doc_type_id: int, db_session):
    query_doc_type = db_session.query(lt_m_doc_type_Base).filter(lt_m_doc_type_Base.doc_type_id==doc_type_id).first()
    return query_doc_type
