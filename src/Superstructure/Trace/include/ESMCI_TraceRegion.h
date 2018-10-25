// $Id$
//
// Earth System Modeling Framework
// Copyright 2002-2018, University Corporation for Atmospheric Research, 
// Massachusetts Institute of Technology, Geophysical Fluid Dynamics 
// Laboratory, University of Michigan, National Centers for Environmental 
// Prediction, Los Alamos National Laboratory, Argonne National Laboratory, 
// NASA Goddard Space Flight Center.
// Licensed under the University of Illinois-NCSA License.

#ifndef ESMCI_TRACEREGION_H
#define ESMCI_TRACEREGION_H

#define ESMF_PROFILE_INTERNAL_off
#ifdef ESMF_PROFILE_INTERNAL
#define ESMCI_METHOD_ENTER(localrc) ESMCI::TraceEventRegionEnter(ESMC_METHOD, &(localrc)); \
  if (ESMC_LogDefault.MsgFoundError(localrc, ESMCI_ERR_PASSTHRU, ESMC_CONTEXT, \
                                    &rc)) return rc;
#define ESMCI_METHOD_EXIT(localrc)  ESMCI::TraceEventRegionExit(ESMC_METHOD, &(localrc)); \
  if (ESMC_LogDefault.MsgFoundError(localrc, ESMCI_ERR_PASSTHRU, ESMC_CONTEXT, \
                                    &rc)) return rc;
#define ESMCI_REGION_ENTER(name, localrc)      ESMCI::TraceEventRegionEnter(name, &(localrc)); \
  if (ESMC_LogDefault.MsgFoundError(localrc, ESMCI_ERR_PASSTHRU, ESMC_CONTEXT, \
                                    &rc)) return rc;
#define ESMCI_REGION_EXIT(name, localrc)       ESMCI::TraceEventRegionExit(name, &(localrc)); \
  if (ESMC_LogDefault.MsgFoundError(localrc, ESMCI_ERR_PASSTHRU, ESMC_CONTEXT, \
                                    &rc)) return rc;
#else
#define ESMCI_METHOD_ENTER(rc)
#define ESMCI_METHOD_EXIT(rc)
#define ESMCI_REGION_ENTER(name, localrc)
#define ESMCI_REGION_EXIT(name, localrc) 
#endif

namespace ESMCI { 
  void TraceEventRegionEnter(std::string name, int *rc);
  void TraceEventRegionExit(std::string name, int *rc);
}

#endif