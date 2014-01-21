/*! \file trace_codes.h 
  
  \copyright Redistribution and use in source and binary forms, with
  or without modification, are permitted provided that the following
  conditions are met:
  
  \copyright Redistributions of source code must retain the above
  copyright notice, this list of conditions and the following
  disclaimer.
  
  \copyright Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following
  disclaimer in the documentation and/or other materials provided with
  the distribution.
  
  \copyright Neither the name of CDBAE nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
  
  \copyright THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
  BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  
*/

#ifndef TRUNK_INCLUDE_TRACER_DETECTOR_TRACE_CODES_H_
#define TRUNK_INCLUDE_TRACER_DETECTOR_TRACE_CODES_H_

#include <vartrace/vartrace.h>

namespace cdbae {
namespace tracer_detector {

//! Идентификаторы переменных в журнале.
enum TracerDetectorMessageIds {
  kMessageIdError,
  kMessageIdInfo
};

//! Идентификаторы нестандартных типов, используемых в журнале.
enum TracerDetectorTypeIds {
  kTypeIdTracerDetector = 0x20,
  kTypeIdErrorEvents,
  kTypeIdInfoEvents
};

enum ErrorEvents {
  kErrorEventMessageQCreate,
  kErrorEventUnknownMessage,
  kErrorEventInvalidDebugRequest,
  kErrorEventDebugSend,
  kErrorEventInvalidFreeRequest
};

enum InfoEvents {
  kInfoEventMasterReady,
  kInfoEventDebugRequest,
  kInfoEventFreeDebugBuffer
};



}  // namespace tracer_detector
}  // namespace cdbae

REGISTER_VARTRACE_TYPE(cdbae::tracer_detector::ErrorEvents,
                       cdbae::tracer_detector::kTypeIdErrorEvents);
REGISTER_VARTRACE_TYPE(cdbae::tracer_detector::InfoEvents,
                       cdbae::tracer_detector::kTypeIdInfoEvents);

#endif  // TRUNK_INCLUDE_TRACER_DETECTOR_TRACE_CODES_H_
