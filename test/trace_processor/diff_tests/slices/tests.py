#!/usr/bin/env python3
# Copyright (C) 2023 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License a
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from python.generators.diff_tests.testing import Path, DataPath, Metric
from python.generators.diff_tests.testing import Csv, Json, TextProto, BinaryProto
from python.generators.diff_tests.testing import DiffTestBlueprint
from python.generators.diff_tests.testing import TestSuite
from google.protobuf import text_format


class Slices(TestSuite):

  def test_thread_slice(self):
    return DiffTestBlueprint(
        trace=Path('trace.py'),
        query="""
        SELECT import('common.slices');

        SELECT name, ts, dur, depth, thread_name, tid, process_name, pid
        FROM thread_slice;
      """,
        out=Csv("""
        "name","ts","dur","depth","thread_name","tid","process_name","pid"
        "ThreadSlice",5,6,0,"Thread",5,"Process",3
      """))

  def test_process_slice(self):
    return DiffTestBlueprint(
        trace=Path('trace.py'),
        query="""
        SELECT import('common.slices');

        SELECT name, ts, dur, depth, process_name, pid
        FROM process_slice;
      """,
        out=Csv("""
        "name","ts","dur","depth","process_name","pid"
        "ProcessSlice",3,4,0,"Process",3
      """))

  def test_slice_with_process_and_thread_info(self):
    return DiffTestBlueprint(
        trace=Path('trace.py'),
        query="""
        SELECT import('experimental.slices');

        SELECT name, ts, dur, depth, thread_name, tid, process_name, pid
        FROM experimental_slice_with_thread_and_process_info;
      """,
        out=Csv("""
        "name","ts","dur","depth","thread_name","tid","process_name","pid"
        "AsyncSlice",1,2,0,"[NULL]","[NULL]","[NULL]","[NULL]"
        "ProcessSlice",3,4,0,"[NULL]","[NULL]","Process",3
        "ThreadSlice",5,6,0,"Thread",5,"Process",3
      """))