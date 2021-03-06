# /usr/bin/env python
"""
Simple synthetic data generator
author: John Ding johnding1996@hotmail.com

The purpose of this script is to attempt to create synthetic JSON tracking logs
that are equally good to test through the apipe and qpipe of MLC.
It can also generates synthetic course files that can be used to test the extension pipes.

This simple synthetic data generator tries to make up data according to edx guide,
while this method works, it only generates independent records and represent no meaningful
information. So the synthetic data generated by this can only be used to test MLC, but not
other pipelines of the MOOC-Learner-Project

The argument after -c is the synthetic course name
The argument after -o is the output data folder path (it must already exists)
The argument after -n is the number of independent records of each synthetic files
Switch on vismooc_extensions file generator by flag -v
Switch on newmitx_extensions file generator by flag -m
"""
import sys
import json
import os
import string
import random
import argparse


# TODO: Share this default file suffix dict among many tools instead of hardcoded

DEFAULT_DATA_FILE_SUFFIX = {'log_file': '_log_data.json',
                            'vismooc_file': {
                                'course_structure_file': '-course_structure-prod-analytics.json',
                                'course_certificates_file': '-certificates_generatedcertificate-prod-analytics.sql',
                                'course_enrollment_file': '-student_courseenrollment-prod-analytics.sql',
                                'course_user_file': '-auth_user-prod-analytics.sql',
                                'course_profile_file': '-auth_userprofile-prod-analytics.sql',
                                'course_forum_file': '-prod.mongo',
                            },
                            'newmitx_file': {
                            },
                            }

AGENT_TYPES = [
    "Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/39.0.2171.95 Safari\/537.36",
    "Dalvik/1.6.0 (Linux; U; Android 4.0.2; sdk Build/ICS_MR0)",
    "Mozilla\/5.0 (Windows NT 6.1; WOW64; Trident\/7.0; rv:11.0) like Gecko",
    "Mozilla\/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko\/20100101 Firefox\/37.0",
]

def gen_log():
    out_filename = os.path.join(out_path + "/", course_name + DEFAULT_DATA_FILE_SUFFIX['log_file'])
    with os.fdopen(
            os.open(out_filename, os.O_CREAT | os.O_TRUNC | os.O_WRONLY),
            'w') as outfile:
        for count in range(num_records):
            encoded_json_line = "%s\n" % gen_one_resource_log()
            encoded_json_line += "%s\n" % gen_one_click_log()
            encoded_json_line += "%s\n" % gen_one_submission_log()
            encoded_json_line += "%s\n" % gen_one_assessment_log()
            outfile.write(encoded_json_line)


def gen_one_resource_log():
    course_code = str(random.randint(1, 20)) + u"." + str(random.randint(0, 999)) + u'x'
    course_term = str(random.randint(2000, 2016)) + u'_' + random.choice([u"Fall", u"Spring"])
    l = dict()
    l[u"username"] = u''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(0, 10)))
    l[u'agent'] = random.choice(AGENT_TYPES)
    l[u"event_source"] = u"server"
    l[u"ip"] = u"{0}.{1}.{2}.{3}".format(str(random.randint(0, 255)),
                                         str(random.randint(0, 255)),
                                         str(random.randint(0, 255)),
                                         str(random.randint(0, 255)))
    l[u"event_type"] = u"/courses/MITx/{0}/{1}/{2}".format(course_code,
                                                           course_term,
                                                           u"".join(random.choice(string.ascii_letters + string.digits)
                                                                    for _ in range(random.randint(0, 10))))
    l[u"time"] = u"{0}-{1}-{2} {3}:{4}:{5}.{6} UTC".format(
        str(random.randint(2010, 2017)),
        str(random.randint(1, 12)).zfill(2),
        str(random.randint(1, 28)).zfill(2),
        str(random.randint(0, 23)).zfill(2),
        str(random.randint(0, 59)).zfill(2),
        str(random.randint(0, 59)).zfill(2),
        str(random.randint(0, 999999)).zfill(6)
    )
    l[u"course_id"] = u"MITx/{0}/{1}".format(course_code,
                                             course_term)
    l[u"_id"] = {u"$oid": u''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24))}
    l[u"event"] = {u"POST": {}, u"GET": {}}

    return json.dumps(l)


def gen_one_click_log():
    course_code = str(random.randint(1, 20)) + u"." + str(random.randint(0, 999)) + u'x'
    course_term = str(random.randint(2000, 2016)) + u'_' + random.choice([u"Fall", u"Spring"])
    CLICK_EVENT_TYPES = [
        'play_video', 'load_video', 'pause_video', 'stop_video',
        'seek_video', 'speed_change_video', 'hide_transcript', 'show_transcript',
        'video_hide_cc_menu', 'video_show_cc_menu'
    ]
    l = dict()
    l[u"username"] = u''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(0, 10)))
    l[u'agent'] = random.choice(AGENT_TYPES)
    l[u"event_source"] = u"server"
    l[u"ip"] = u"{0}.{1}.{2}.{3}".format(str(random.randint(0, 255)),
                                         str(random.randint(0, 255)),
                                         str(random.randint(0, 255)),
                                         str(random.randint(0, 255)))
    l[u"event_type"] = random.choice(CLICK_EVENT_TYPES)
    l[u"time"] = u"{0}-{1}-{2} {3}:{4}:{5}.{6} UTC".format(
        str(random.randint(2010, 2017)),
        str(random.randint(1, 12)).zfill(2),
        str(random.randint(1, 28)).zfill(2),
        str(random.randint(0, 23)).zfill(2),
        str(random.randint(0, 59)).zfill(2),
        str(random.randint(0, 59)).zfill(2),
        str(random.randint(0, 999999)).zfill(6)
    )
    l[u"course_id"] = u"MITx/{0}/{1}".format(course_code,
                                             course_term)
    l[u"_id"] = {u"$oid": u''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24))}
    l[u"event"] = {
        u'id': u''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24)),
        u'code': u''.join(random.choice(string.ascii_letters) for _ in range(12)),
        u'currentTime': str(random.randint(0, 3600))
    }
    l[u'context'] = {
        u'org_id': u'MITx',
        u'path': u'/event',
        u'course_id': u"MITx/{0}/{1}".format(course_code,
                                             course_term),
        u'user_id': str(random.randint(0, 99999999)).zfill(8)
    }

    return json.dumps(l)


def gen_one_submission_log():
    course_code = str(random.randint(1, 20)) + u"." + str(random.randint(0, 999)) + u'x'
    course_term = str(random.randint(2000, 2016)) + u'_' + random.choice([u"Fall", u"Spring"])
    SUBMISSION_EVENT_TYPES = [
        'problem_check', 'problem_check_fail', 'problem_reset',
        'reset_problem', 'problem_save', 'problem_show', 'showanswer',
        'save_problem_fail', 'save_problem_success', 'problem_graded',
        'i4x_problem_input_ajax', 'i4x_problem_problem_check',
        'i4x_problem_problem_get', 'i4x_problem_problem_reset',
        'i4x_problem_problem_save', 'i4x_problem_problem_show',
        'oe_hide_question', 'oe_show_question', 'rubric_select',
        'i4x_combinedopenended_some_action', 'peer_grading_some_action',
        'staff_grading_some_action', 'i4x_peergrading_some_action'
    ]
    l = dict()
    l[u"username"] = u''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(0, 10)))
    l[u'agent'] = random.choice(AGENT_TYPES)
    l[u"event_source"] = u"server"
    l[u"ip"] = u"{0}.{1}.{2}.{3}".format(str(random.randint(0, 255)),
                                         str(random.randint(0, 255)),
                                         str(random.randint(0, 255)),
                                         str(random.randint(0, 255)))
    l[u"event_type"] = random.choice(SUBMISSION_EVENT_TYPES)
    l[u"time"] = u"{0}-{1}-{2} {3}:{4}:{5}.{6} UTC".format(
        str(random.randint(2010, 2017)),
        str(random.randint(1, 12)).zfill(2),
        str(random.randint(1, 28)).zfill(2),
        str(random.randint(0, 23)).zfill(2),
        str(random.randint(0, 59)).zfill(2),
        str(random.randint(0, 59)).zfill(2),
        str(random.randint(0, 999999)).zfill(6)
    )
    l[u"course_id"] = u"MITx/{0}/{1}".format(course_code,
                                             course_term)
    l[u"_id"] = {u"$oid": u''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24))}
    l[u"event"] = {
        u'problem': u''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24)),
    }
    l[u'context'] = {
        u'org_id': u'MITx',
        u'path': u'/event',
        u'course_id': u"MITx/{0}/{1}".format(course_code,
                                             course_term),
        u'user_id': str(random.randint(0, 99999999)).zfill(8)
    }

    return json.dumps(l)


def gen_one_assessment_log():
    course_code = str(random.randint(1, 20)) + u"." + str(random.randint(0, 999)) + u'x'
    course_term = str(random.randint(2000, 2016)) + u'_' + random.choice([u"Fall", u"Spring"])
    ASSESSMENT_EVENT_TYPES = [
        'save_problem_check', 'problem_check'
    ]
    l = dict()
    l[u"username"] = u''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(0, 10)))
    l[u'agent'] = random.choice(AGENT_TYPES)
    l[u"event_source"] = u"server"
    l[u"ip"] = u"{0}.{1}.{2}.{3}".format(str(random.randint(0, 255)),
                                         str(random.randint(0, 255)),
                                         str(random.randint(0, 255)),
                                         str(random.randint(0, 255)))
    l[u"event_type"] = random.choice(ASSESSMENT_EVENT_TYPES)
    l[u"time"] = u"{0}-{1}-{2} {3}:{4}:{5}.{6} UTC".format(
        str(random.randint(2010, 2017)),
        str(random.randint(1, 12)).zfill(2),
        str(random.randint(1, 28)).zfill(2),
        str(random.randint(0, 23)).zfill(2),
        str(random.randint(0, 59)).zfill(2),
        str(random.randint(0, 59)).zfill(2),
        str(random.randint(0, 999999)).zfill(6)
    )
    l[u"course_id"] = u"MITx/{0}/{1}".format(course_code,
                                             course_term)
    l[u"_id"] = {u"$oid": u''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24))}
    problem_id = u''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(24))
    l[u"event"] = {
        u'answers': {problem_id: u'choice_0'},
        u'attempts': random.randint(0, 100),
        u'correct_map': {problem_id: {
            u'correctness': random.choice([u'correct', u'incorrect']),
            u'hint': u'',
            u'hintmode': None,
            u'msg': u'',
            u'npoints': 0,
            u'queuestate': None
        }},
        u'grade': 0,
        u'max_grade': 0,
        u'problem_id': problem_id,
        u'state': {},
        u'success': random.choice([u'correct', u'incorrect']),
    }
    l[u'context'] = {
        u'org_id': u'MITx',
        u'path': u'/event',
        u'course_id': u"MITx/{0}/{1}".format(course_code,
                                             course_term),
        u'user_id': str(random.randint(0, 99999999)).zfill(8)
    }

    return json.dumps(l)


# TODO: write code to generate simple synthetic data files for extension pipes

def gen_vismooc():
    pass


def gen_newmitx():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate sample synthetic data to test MLC.')
    parser.add_argument("-c", action="store", default='synthetic', dest='course_name',
                        help='synthethic course name')
    parser.add_argument('-o', action='store', default=os.path.join(os.path.realpath(__file__), '../../../'),
                        dest='out_path', help='path to data folder, default: the parent folder of MLC')
    parser.add_argument('-n', action='store', default=1000, type=int, dest='num_records',
                        help='number of records of all synthetic data files, default 1000')
    parser.add_argument('-v', action='store_true', default=False, dest='shall_gen_vismooc',
                        help='switch on to generate synthetic data files for vismooc extensions')
    parser.add_argument('-m', action='store_true', default=False, dest='shall_gen_newmitx',
                        help='switch on to generate synthetic data files for newmitx extensions')
    course_name = parser.parse_args().course_name
    out_path = parser.parse_args().out_path
    num_records = parser.parse_args().num_records
    shall_gen_vismooc = parser.parse_args().shall_gen_vismooc
    shall_gen_newmitx = parser.parse_args().shall_gen_newmitx

    out_path = os.path.abspath(out_path)
    if not os.path.isdir(out_path):
        sys.exit('Output data directory does not exist')

    out_path = os.path.join(out_path + "/", 'data')
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_path = os.path.join(out_path + "/", course_name)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    print('Generated synthetic course path: %s' % out_path)
    out_path = os.path.join(out_path + "/", 'log_data')
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    gen_log()

    if shall_gen_vismooc:
        gen_vismooc()
    if shall_gen_newmitx:
        gen_newmitx()

