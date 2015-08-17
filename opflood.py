#!/usr/bin/env python
# coding=utf-8
__author__ = 'yxryab'
import logging
import optparse
import re
import sys
import platform
import os
from collections import OrderedDict
from time import gmtime, strftime
from subprocess import Popen, PIPE, CalledProcessError, call
def checkExcept(results):
    resultERROR = []
    resultSUCCSES = []
    resultDic = resultMain
    for result in results:
        logging.info(result)
        try:
            errore = reerror.findall(str(result))
            unknownCommand = reunkcom.findall(str(result))
            oshibka = reoshibka.findall(result.decode('utf-8'))
            nofile = renofile.findall(result.decode('utf-8'))
            neudalos = reneudalos.findall(result.decode('utf-8'))
        except re.error, e:
            logging.info("Error regular expression %s" % e)
        try:
            if errore or unknownCommand or oshibka or nofile or neudalos:
                f = open('/opt/opflood/log/' + (strftime("%d_%m_%Y", gmtime())) + '.log', 'a')
                global openfile
                openfile = True
                if neudalos:
                    resultERROR.append(neudalos[0] + ", and still found: '" + str(len(neudalos)) + "' errors in stdout, schema: " + schema)
                if errore:
                    resultERROR.append(errore[0] + ", and still found: '" + str(len(errore)) + "' errors in stdout, schema: " + schema)
                if unknownCommand:
                    resultERROR.append(unknownCommand[0] + ", and still found: '" + str(len(unknownCommand)) + "' errors in stdout, schema: " + schema)
                if oshibka:
                    resultERROR.append(oshibka[0] + u", and still found: '" + str(len(oshibka)) + u"' errors in stdout, schema: " + schema)
                if nofile:
                    resultERROR.append(nofile[0] + u", and still found: '" + str(len(nofile)) + u"' errors in stdout, schema: " + schema)
                f.write(str((strftime("%d/%m/%Y %H:%M:%S", gmtime()) + ' - in schema: ' + schema + " errors " + str(result))))
                f.close()
            else:
                resultSUCCSES.append("No errors were found in schema: %s" % schema)
        except TypeError, e:
            logging.info('Errors %s' % e)
    if len(resultERROR) == 0:
        resultDic.update({
            schema: schema,
            schema + 'errors': False,
            schema + 'succses': resultSUCCSES
        })
    elif len(resultERROR) >= 1:
        resultDic.update({
            schema: schema,
            schema + 'errors': resultERROR,
            schema + 'succses': resultSUCCSES
        })
    return resultDic
def runSqlQueryOracle(sqlCommand, connectString):
    try:
        session = Popen(['sqlplus', '-S', connectString], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        session.stdin.write(sqlCommand)
    except CalledProcessError, e:
        logging.info("Failure: %s" % e)
        sys.exit(1)
    return session.communicate()
def runSqlQueryPostgresql(connectSring, sqlCommand):
    try:
        os.environ['PGPASSWORD'] = password
        session = Popen(connectSring + sqlCommand, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    except CalledProcessError, e:
        logging.info("Failure: %s" % e)
        sys.exit(1)
    return session.communicate()
def installComponents():
    def ErrorMessage(ec):
        logging.info("Installation ended with error, exit_code: %s" % str(ec))
        sys.exit(1)
    currentPlatform = (platform.dist()[0].lower())
    currentRelease = (platform.dist()[1].split('.')[0])
    postgresURL = ('http://yum.postgresql.org/9.4/redhat/rhel-%s-x86_64/pgdg-%s94-9.4-1.noarch.rpm' % (currentRelease, currentPlatform))
    ExitCodePostgres = call(['rpm', '-q', 'postgresql94'], stdout=PIPE)
    ExitCodeNonVersionPostgres = call(['rpm', '-q', 'postgresql'], stdout=PIPE)
    ExitCodeSqlplus = call(['rpm', '-q', 'oracle-instantclient12.1-sqlplus-12.1*'], stdout=PIPE)
    ExitCodeBasic = call(['rpm', '-q', 'oracle-instantclient12.1-basic-12.1*'], stdout=PIPE)
    ExitCodePostgresInstallRepo = call(['rpm', '-q', 'pgdg-centos94-9.4-1'], stdout=PIPE)
    try:
        if "postgresql" == install or "all" == install:
            if 0 == ExitCodeNonVersionPostgres:
                o = Popen(['rpm', '-q', 'postgresql'], stdout=PIPE)
                ovp, err = o.communicate()
                logging.info("You have installed %s, to work correctly, remove the old version of PostgreSQL" % ovp.strip())
                logging.info("Installation failed because the tasks required under the terms of PostgreSQL 9.4")
                sys.exit(1)
            if 0 == ExitCodePostgres:
                logging.info('PostgreSQL 9.4 already installed')
            else:
                if 0 == ExitCodePostgresInstallRepo:
                    logging.info("PostgreSQL 9.4 repo, already installed")
                else:
                    ExitCodePostgresInstallRepo = call(['yum', 'install', postgresURL, '-y'])
                if 0 == ExitCodePostgresInstallRepo:
                    ExitCodePostgresInstallPostgres = call(['yum', 'install', 'postgresql94', '-y'])
                    if 0 != ExitCodePostgresInstallPostgres:
                        ErrorMessage(ExitCodePostgresInstallPostgres)
                else:
                    ErrorMessage(ExitCodePostgresInstallRepo)
        if "oracle" == install or "all" == install:
            if 0 == ExitCodeBasic:
                logging.info('oracle instantclient 12.1 basic already installed')
            else:
                ExitCodeBasicInstall = call(['yum', 'localinstall', '--nogpgcheck', '-y', '/opt/opflood/archive/oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm'])
                if 0 != ExitCodeBasicInstall:
                    ErrorMessage(ExitCodeBasicInstall)

            if 0 == ExitCodeSqlplus:
                logging.info('oracle instantclient 12.1 sqlplus already installed')
            else:
                ExitCodeSqlplusInstall = call(['yum', 'localinstall', '--nogpgcheck', '-y', '/opt/opflood/archive/oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm'])
                if 0 == ExitCodeSqlplusInstall:
                    call(['cp', '/opt/opflood/archive/sqlplusenv.sh', '/etc/profile.d/sqlplusenv.sh'])
                    logging.info('------------------------------------------------------------------------------------------')
                    logging.info('| In order to successfully work with the Oracle database , you must supply a valid Hosts.|')
                    logging.info('| Example   /etc/hosts:                                                                  |')
                    logging.info('| 127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4         |')
                    logging.info('| ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6         |')
                    logging.info('| 127.0.0.1   hostname                                                                   |')
                    logging.info('------------------------------------------------------------------------------------------')
                    call(['su', '-c', 'source /etc/profile.d/sqlplusenv.sh'], shell=True, executable="/bin/bash")
                else:
                    ErrorMessage(ExitCodeSqlplusInstall)
    except OSError, e:
        logging.info(e)
        sys.exit(1)
    sys.exit(0)
if __name__ == '__main__':
    parser = optparse.OptionParser(usage="usage: %prog [-h] [-a ADDRESS] \n\
                  [-p PORT] [-u USER] [-w PASSWORD] [--install]\n\
                  [-i DIALECT] [-d DATABASE] [-s SCHEMA] [-v VERBOSE] [-q QUIET] [--version]",
                                    version="%prog 1.2",
                                    description='The script contains a minimum set of customers for \
                                    PostgreSQL and Oracle. Designed for use SQL injection. \
                                    Example: \
                                    \
                                    Oracle: ./%prog -i oracle -a 10.0.0.1 -u system -w 123456 -d dbt -s 1.sql -s /schem/2.sql \
                                    \
                                    PostgreSQL: ./%prog -i postgresql -a 10.0.0.2 -u system -w 123456 -d dbt -s 1.sql -s /shem/2.sql \
                                                ')
    parser.add_option("-a", "--address", dest="address", metavar="Server address",
                      default='localhost', type="string",
                      help="Server address, default 'localhost'")
    parser.add_option("-p", "--port", dest="port", type="string",
                      help="Server port")
    parser.add_option("-u", "--user", dest="user", type="string",
                      help="username")
    parser.add_option("-w", "--password", dest="password", type="string",
                      help="Password")
    parser.add_option("-i", "--dialect", metavar="{oracle or postgresql}", dest="dialect",
                      choices=("oracle", "postgresql"), help="Dialect of SQL {oracle, postgresql}")
    parser.add_option("-d", "--db", metavar="DB name", dest="db", type="string",
                      help="Name the connected database")
    parser.add_option("-s", "--schema", dest="schema", action="append",
                      help="Database schema name(s)")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet", action="store_false", dest="verbose")
    parser.add_option("--install", dest="install", choices=("oracle", "postgresql", "all"), metavar="{oracle or postgresql or all}", help="Installing components")
    (options, args) = parser.parse_args()
    address = options.address
    port = options.port
    user = options.user
    password = options.password
    dialect = options.dialect
    db = options.db
    schemas = options.schema
    install = options.install
    resultMain = {}
    openfile = False
    if options.verbose is None:
        logging.basicConfig(format='%(asctime)s : %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.INFO,
                            stream=sys.stdout)
    elif options.verbose:
        logging.basicConfig(format='%(asctime)s : %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            level=logging.DEBUG,
                            stream=sys.stdout)
    else:
        logging.basicConfig(format='%(asctime)s : %(message)s',
                            datefmt='%m/%d/%Y %H:%M:%S',
                            filename=("/opt/opflood/log/" + strftime("%d_%m_%Y", gmtime()) + ".log"),
                            level=logging.DEBUG)
    def parsExcept():
        parser.print_help()
        sys.exit(1)
    resultFinish = []
    reerror = re.compile('.*ERROR|error|FATAL|fatal|FAILED|failed|exception|EXCEPTION|critical|CRITICAL.*')
    reunkcom = re.compile('.*unknown|unable\ to\ open.*')
    uni1 = u"ОШИБКА"
    reoshibka = re.compile(".*" + uni1 + ".*")
    uni2 = u"Нет такого файла"
    renofile = re.compile('.*' + uni2 + '.*')
    uni3 = u"не удалось"
    reneudalos = re.compile('.*' + uni3 + '.*')
    if install:
        if os.getegid() == 0:
            installComponents()
        else:
            logging.info("You need to have root privileges to run installation. Please try again, this time using 'sudo'.")
            sys.exit(1)
    if not schemas:
        logging.info("To work correctly, need SQL schema")
        parsExcept()
    if 'localhost' == address:
        logging.info("The script will run on localhost")
    if not db:
        logging.info("To work correctly, need database name")
        parsExcept()
    if not dialect:
        logging.info("Looking for information about the database server")
        parsExcept()
    logging.info('Connect and SQL script execution may take time')
    for schema in schemas:
        if 'oracle' == dialect:
            if not port:
                port = '1521'
            connectSring = ('%s/%s@%s:%s/%s' % (user, password, address, port, db))
            sqlCommand = ('@%s' % schema)
            results = runSqlQueryOracle(sqlCommand, connectSring)
            resultMain.update(checkExcept(results))
        if 'postgresql' == dialect:
            if not port:
                port = '5432'
            sqlCommand = ['-f', schema]
            if 'localhost' == address:
                connectSring = ['psql', '-U', user, '-d', db]
            else:
                connectSring = ['psql', '-h', address, '-p', port, '-U', user, '-d', db]
            results = runSqlQueryPostgresql(connectSring, sqlCommand)
            os.environ['PGPASSWORD'] = ''
            resultMain.update(checkExcept(results))
    if True == openfile:
        logging.info("---in total------- Please refer to the log in: /opt/opflood/log/" + str((strftime("%d_%m_%Y", gmtime()))) + ".log----------")
    else:
        logging.info("---in total-------------------------------------------------------")
    for schema in schemas:
        if resultMain[schema + 'errors']:
            for re in resultMain[schema + 'errors']:
                logging.info(re)
        else:
            for rs in list(OrderedDict.fromkeys(resultMain[schema + 'succses'])):
                logging.info(rs)