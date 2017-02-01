#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Tiago de Freitas Pereira <tiago.pereira@idiap.ch>
# @date:   Tue Aug  11 14:07:00 CEST 2015
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This script creates the Periocular Recognition competition"""

import os
import numpy
numpy.random.seed(10)
from .models import *
from .models import PROTOCOLS, GROUPS, PURPOSES
import pkg_resources
import bob.io.base.test_utils


def _update(session, field):
    """Add, updates and returns the given field for in the current session"""
    session.add(field)
    session.flush()
    session.refresh(field)
    return field


def add_clients_files(session, image_dir, verbose=True):
    """
    Add the clients and files in one single shot

    """

    clients = {}  # Controling the clients and the sessions captured for each client
    file_id_offset = 1

    data_files = [bob.io.base.test_utils.datafile('NIR.txt', __name__),
                  bob.io.base.test_utils.datafile('VIS.txt', __name__)]

    for f in data_files:

        if f.find("NIR") >= 0:
            modality = "NIR"
        else:
            modality = "VIS"

        for c in open(f).readlines():

            # Generation the client name R-XXX or L-XXX
            client_name = c.split("/")[-3] + "-" + c.split("/")[-2]
            if not clients.has_key(client_name):
                clients[client_name] = []
                if verbose >= 1: print("  Adding client {0}".format(client_name))
                session.add(Client(id=client_name))

            file_list = os.listdir(os.path.join(image_dir, c).rstrip("\n"))
            for ff in file_list:
                file_name = os.path.join(c.rstrip("\n"), os.path.splitext(ff)[0])
                if verbose >= 1: print("  Adding file {0}".format(file_name))
                session.add(File(file_id_offset, file_name, client_name, modality))
                clients[client_name].append(file_id_offset)
                file_id_offset += 1

    return clients


def add_protocols(session, clients, protocol):

    keys = clients.keys()
    numpy.random.shuffle(keys)

    # Adding world
    for i in range(0, 20):
        files = clients[keys[i]]

        for f in files:
            session.add(Protocol_File_Association(protocol, "world", "train", f))

    # Adding dev
    for i in range(20, 30):
        files = clients[keys[i]]
        enroll = True
        for f in files:
            if enroll:
                purpose="enroll"
                enroll = False
            else:
                purpose="probe"

            session.add(Protocol_File_Association(protocol, "dev", purpose, f))

    # Adding dev
    for i in range(30, 40):
        files = clients[keys[i]]
        enroll = True
        for f in files:
            if enroll:
                purpose = "enroll"
                enroll = False
            else:
                purpose = "probe"

            session.add(Protocol_File_Association(protocol, "eval", purpose, f))


def create_tables(args):
    """Creates all necessary tables (only to be used at the first time)"""

    from bob.db.base.utils import create_engine_try_nolock

    engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2));
    Client.metadata.create_all(engine)
    File.metadata.create_all(engine)
    Protocol_File_Association.metadata.create_all(engine)


# Driver API
# ==========

def create(args):
    """Creates or re-creates this database"""

    from bob.db.base.utils import session_try_nolock

    dbfile = args.files[0]

    if args.recreate:
        if args.verbose and os.path.exists(dbfile):
            print('unlinking %s...' % dbfile)
        if os.path.exists(dbfile): os.unlink(dbfile)

    if not os.path.exists(os.path.dirname(dbfile)):
        os.makedirs(os.path.dirname(dbfile))

    # the real work...
    create_tables(args)
    s = session_try_nolock(args.type, args.files[0], echo=(args.verbose >= 2))
    clients = add_clients_files(s, args.image_dir, args.verbose)
    add_protocols(s, clients, "cross-eye-VIS-NIR-split1")
    add_protocols(s, clients, "cross-eye-VIS-NIR-split2")
    add_protocols(s, clients, "cross-eye-VIS-NIR-split3")
    add_protocols(s, clients, "cross-eye-VIS-NIR-split4")
    add_protocols(s, clients, "cross-eye-VIS-NIR-split5")

    s.commit()
    s.close()


def add_command(subparsers):
    """Add specific subcommands that the action "create" can use"""

    parser = subparsers.add_parser('create', help=create.__doc__)

    parser.add_argument('-r', '--recreate', action='store_true', help='If set, I\'ll first erase the current database')
    parser.add_argument('-v', '--verbose', action='count', help='Increase verbosity?')
    parser.add_argument('-d', '--image-dir', default='/idiap/project/hface/databases/CrossEyed2016TrainSet/PeriCrossEyed/',
                        help="Change the relative path to the directory containing the images of the Cross Spectral Database.")

    parser.set_defaults(func=create)  # action
