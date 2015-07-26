#!/usr/bin/sh
#|---------------------------------------------------------------------|#
#|  SCRIPT NAME:  get_legislators.sh                                  |#
#|  AUTHOR:       Krishna Balam                                        |#
#|  CREATE DATE:  07/25/2015                                           |#
#|---------------------------------------------------------------------|#
#|  PURPOSE:                                                           |#
#|                This script downloads one json file for all MPs from |#
#|                indian parliment both loksabha and rajya sabha page  |#
#|                by page and Later on it concatenates all the files.  |#
#|                It also includes logic to incorporate page size limit|#
#|                from sansad API.It uses Linux CURL command to post   |#
#|                and get results from API                             |#
#|                                                                     |#
#|  FUNCTIONS:                                                         |#
#|                drop_prev_file                                       |#
#|                call_api                                             |#
#|  ARGUMENTS:                                                         |#
#|              - JOB_DATE in YYYYMMDD format                          |#
#|                                                                     |#
#|  RETURNS:                                                           |#
#|              - 0 (SUCCESS)                                          |#
#|              - 1 (FAIL)                                             |#
#|                                                                     |#
#|---------------------------------------------------------------------|#
#|                                                                     |#
#|  CHANGES:                                                           |#
#|  ----------  --- -------------------------------------------------  |#
#|  2015-07-25  KKB Initial creation                                   |#
#\---------------------------------------------------------------------/#

#/---------------------------------------------------------------------\#
#|                                                                     |#
#| LOCAL FUNCTIONS                                                     |#
#|                                                                     |#
#\---------------------------------------------------------------------/#


#********************************************************************#
#  FUNCTION log message
#********************************************************************#
logmsg()
{
  export MSG_STR=$1
  echo ${MSG_STR} >> ${LOGFILE_NAME}
} 

#********************************************************************#
#  FUNCTION check return code
#********************************************************************#
check_retcode()
{
  export ret_code_string=$1
  export message=$2
  export mail_flg=$3

  logmsg "return code from prev command is: ${ret_code_string}"
  logmsg "Message for previous command is: ${message}"
  logmsg "Mail falg is ${mail_flg}"
  
  #Temporary file for containing the mail message

  TO="krushna.balam@gmail.com"
  SUBJECT="${INTERFACE_NAME}: ${message} FAILED "
  
  if [[ "$ret_code_string" -ne "0" ]] 
  then
    logmsg "$SUBJECT"
    
    if [[ "$mail_flg" -eq "Y" ]] 
    then
    		logmsg "Sending failure Email"
    		if ( -f $MAILFILE ) then
                  rm $MAILFILE
                fi
  			touch $MAILFILE
  			chmod 600 $MAILFILE
    		echo -e "${SUBJECT} on $DATE_KEY" > $MAILFILE
    		/bin/mail -s "$SUBJECT" "$TO" < $MAILFILE
    		exit 1
    fi
   else
    logmsg "$message SUCCESSFUL"
  fi
} 

#********************************************************************#
#  FUNCTION drop_prev_file
#********************************************************************#
drop_prev_file()
{
      export STEP_NUM=$1
      logmsg "=============================================="
      logmsg "Starting step >${STEP_NUM}< --  ${0} "
   
      if [[ -e "${DATAFILE}*" ]] 
      then   
       rm "${DATAFILE}"*.json
       check_retcode "$?" "${INTERFACE_NAME}:  Removing previous day file >${STEP_NUM}<" "N"
      fi
      
      touch ${DATAFILE}.json 
      check_retcode "$?" "${INTERFACE_NAME}:  touch today file >${STEP_NUM}<" "N"
      
      chmod 700 ${DATAFILE}.json 
      check_retcode "$?" "${INTERFACE_NAME}:  Change permissions on the files >${STEP_NUM}<" "N"
      
      logmsg "Completed Step:${STEP_NUM} SUCCESSFULLY"
}  


#********************************************************************#
#  FUNCTION call_detail_api
#********************************************************************#
calculate_num_of_pages()
{
   
   export file_to_use=${1}

   logmsg "============================================"
   logmsg "Calculating number of pages for ${API_MODULE}"
   logmsg "File being used is ${file_to_use}"
   
   export total=`/usr/bin/jq '.count' < ${SUMMARY_FILE}`
   check_retcode "$?" "${INTERFACE_NAME}:  Exporting total number of rows for the module ${API_MODULE} for Clinet ${CLIENT_ID} and department ${DEPT_ID} : >${STEP_NUM}<" "Y"
        
   logmsg "total number of rows are ${total}"
        
   if [[ $total -eq "0" ]]                        
   then
     num_of_pages=0
   else
     num_of_pages=$(( total / PAGESIZE ))
     check_retcode "$?" "${INTERFACE_NAME}:  Calculating initial num of pages for the module ${API_MODULE} : >${STEP_NUM}<" "Y"
     logmsg "number of pages for total rows ${total} with page size ${PAGESIZE} is ${num_of_pages}"
     num_of_pages=$((num_of_pages + 1))
   #   num_of_pages=1
     check_retcode "$?" "${INTERFACE_NAME}:  Calculating final num of pages for the module ${API_MODULE} : >${STEP_NUM}<" "Y"
     logmsg "Number of pages for the module ${API_MODULE} is ${num_of_pages}"
   fi
}

#********************************************************************#
#  FUNCTION remove_unwated_data
#********************************************************************#
concatenate_data()
{
  export SOURCE_FILE=$1
  export DEST_FILE=$2
  
  logmsg "The source file is $SOURCE_FILE"
  logmsg "Starting to strip first line from the source file"
  logmsg "Destination file is $DEST_FILE"
  
  TMP_SRC_FILE="${SOURCE_FILE}"_TMP

  cat ${SOURCE_FILE} | /usr/bin/jq '.results[]'  > ${TMP_SRC_FILE}
  check_retcode "$?" "${INTERFACE_NAME}:  Removing unnecessary json objects from the file ${API_MODULE} : >${STEP_NUM}<" "Y"
 
  cat ${TMP_SRC_FILE}  >> $DEST_FILE
  check_retcode "$?" "${INTERFACE_NAME}:  Inserting data into final file ${API_MODULE} : >${STEP_NUM}<" "Y"
  
  rm $TMP_SRC_FILE
  logmsg "${INTERFACE_NAME}:  Removing temp file from the folder ${API_MODULE} for : >${STEP_NUM}<"
 
  logmsg "Completed caoncatenating data into the final file"
}

#********************************************************************#
#  FUNCTION call_curl
#********************************************************************#
call_curl()
{
  
  export SOURCE_URL=$2
  export DEST_FILE=$1
  # PROXY_URL=$3
  logmsg "============================================"
  logmsg "Starting to extract data using CURL source"
  logmsg "URL is: ${SOURCE_URL}"
  logmsg "Destination File is: ${DEST_FILE}"
  
  curl  -o ${DEST_FILE} --url "${SOURCE_URL}"
  check_retcode "$?" "${INTERFACE_NAME}:  Extracting data using CURL for ${API_MODULE} Summary : >${STEP_NUM}<" "Y"
  
  logmsg "Extracted data for ${SOURCE_URL} SUCCESSFULLY"

}    
  
#********************************************************************#
#  FUNCTION call_detail_api
#********************************************************************#
call_detail_api ()
{
    export PAGE_NUM=$1

        logmsg "=============================================="
        logmsg "Starting extraction of Page >${PAGE_NUM}< --  ${0} "

        export DETAIL_URL="${API_BASE_URL}/${API_MODULE}?per_page=${PAGESIZE}&page=${PAGE_NUM}"        
        export DETAIL_FILE="${DATAFILE}_${PAGE_NUM}.json"
        
        # Call the function call_curl
        call_curl ${DETAIL_FILE} ${DETAIL_URL}
       
        final_file="${DATAFILE}".json

        #call the function to concatenate data into final file
        concatenate_data ${DETAIL_FILE} ${final_file}
        
        logmsg "Completed Step:${STEP_NUM} SUCCESSFULLY "

}

#********************************************************************#
#  FUNCTION call_api
#********************************************************************#
call_api ()
{
    export STEP_NUM=$1

        logmsg "Starting step >${STEP_NUM}< --  ${0} "


               export SUMMARY_URL="${API_BASE_URL}/${API_MODULE}?per_page=1&page=1"             

        logmsg "Summary URL is $SUMMARY_URL"       
 
        export SUMMARY_FILE="${DATAFILE}_Summary.json"
        logmsg "Summary File is $SUMMARY_FILE"
  
        export num_of_pages=0
        
        ##curl -x ${API_PROXY} -o ${SUMMARY_FILE} --url "${SUMMARY_URL}"
        
        		#Call the function Call_Curl
                        call_curl ${SUMMARY_FILE}  ${SUMMARY_URL}
        
                        #call the funtion calculate_num_of_pages
                        calculate_num_of_pages ${SUMMARY_FILE}
                        
        		export j=1 
        
        		while (( j <= ${num_of_pages} )) ; do
          
          			call_detail_api $j   ## call the detail API function
        
          			j=$((j + 1))
        
        		done

logmsg "Completed Step:${STEP_NUM} SUCCESSFULLY "
logmsg "================================================================="

}
  

#/*********************************************************************\#
#|                                                                     |#
#| MAIN                                                                |#
#|                                                                     |#
#\*********************************************************************/#
#-- Check Arguments

if [ $# -ne 1 ]
then
   echo "Usage:"
   echo "${0} <JOB_DATE_MM/DD/YYYY>"
   exit 1
fi

export BASENAME=${0}
export JOB_DATE=${1}      ## Example: 07/20/2015
export API_MODULE="legislators"    ## Example: ligislatures, bills, discussions
export API_BASE_URL="http://sansad.co/api"


#-- Define variables
export BASE_FOLDER="/home/kbalam/learning/Python"
export DATA_FOLDER="${BASE_FOLDER}/sansad_data"
export INTERFACE_NAME="Sansad_${API_MODULE}"
export DT_LOG_DIR="${BASE_FOLDER}/sansad_data/log"
export MAILFILE="/tmp/${INTERFACE_NAME}_mail.dat"
export DATE_KEY=`date +%Y%m%d`
export LOGFILE_NAME="${DT_LOG_DIR}/${INTERFACE_NAME}_${DATE_KEY}.log"
export DATAFILE="${DATA_FOLDER}/${INTERFACE_NAME}"
export PAGESIZE=50
#-- Start the processing
logmsg "==============================================" 
logmsg "Starting ${0}" 
logmsg "==============================================" 

logmsg "DT LOG DIR is >${DT_LOG_DIR}<"
logmsg "JOB DATE     is >${JOB_DATE}<" 
logmsg "API MODULE is >${API_MODULE}<" 
logmsg "API BASE URL is >${API_BASE_URL}<"
logmsg "DATA FILE is >${DATAFILE}"


#--  Call functions for processing
#--  Usage:  >function< >step number<

#-- STEP 1
drop_prev_file 1

#-- STEP 2
call_api 2 # Call API function
 

#logmsg "Converting json file to csv"


logmsg "=============================================="
logmsg "End of ${0}"
logmsg "=============================================="


       export removal_string="${DATAFILE}_*.json"
       logmsg "Removing temporary files using the string ${removal_string}"
       rm ${removal_string}

exit 0