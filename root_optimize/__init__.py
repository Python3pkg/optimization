#!/usr/bin/env python
# -*- coding: utf-8 -*-,



__version__ = '0.5.1'
__all__ = ['json_encoder',
           'utils']

# Set up ROOT
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import logging
from .utils import TqdmLoggingHandler
logger = logging.getLogger("root_optimize")
logger.addHandler(TqdmLoggingHandler())
