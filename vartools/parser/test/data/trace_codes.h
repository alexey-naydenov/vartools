/*! \file trace_codes.h 
  
  \copyright Copyright 2012 CDBAE, Tula, Russia
  
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
  
  \author Alexey Naydenov
  
  \date 25.10.2012
  
  \brief Коды для логов.
  
*/

#ifndef TRUNK_INCLUDE_TRACER_DETECTOR_TRACE_CODES_H_
#define TRUNK_INCLUDE_TRACER_DETECTOR_TRACE_CODES_H_

#include <vartrace/vartrace.h>

namespace cdbae {
namespace tracer_detector {

//! Идентификаторы переменных в журнале.
enum TracerDetectorMessageIds {
  kMessageIdError,
  kMessageIdInfo,
  kMessageIdMessage,
  kMessageIdMessageSize,
  kMessageIdCompletionCode,
  kMessageIdHeapFree,
  kMessageIdHeapLargestFree,
  kMessageIdMaxStackUsed,
  kMessageIdTaskId,
  kMessageIdDistanceCount,
  kMessageIdMarkerCount,
  kMessageIdFilterCore,
  kMessageIdFilterQueue,
  kMessageIdLookerCore,
  kMessageIdLookerQueue,
  kMessageIdDumpValue
};

//! Идентификаторы нестандартных типов, используемых в журнале.
enum TracerDetectorTypeIds {
  kTypeIdTracerDetector = 0x20,
  kTypeIdErrorEvents,
  kTypeIdInfoEvents,
  kTypeIdMessageEvents
};

enum MessageEvents {
  kMessageEventUnspecified,
  kMessageEventIdleLooker,
  kMessageEventUpdateTask,
  kMessageEventUpdateConfig,
  kMessageEventFindTracers,
  kMessageEventAddTracers,
  kMessageEventBecomeFilter,
  kMessageEventAllDataReceived,
  kMessageEventProcessMarkers,
  kMessageEventDebugRequest,
  kMessageEventDebugTaskResults,
  kMessageEventFreeDebugBuffer,
  kMessageEventRawDataBlock,
  kMessageEventRawDataRequest,
  kMessageEventForwardRawData,
  kMessageEventTest,
  kMessageEventCount
};

enum ErrorEvents {
  kErrorEventMessageQCreate,
  kErrorEventUnknownMessage,
  kErrorEventInvalidDebugRequest,
  kErrorEventDebugSend,
  kErrorEventInvalidFreeRequest,
  kErrorEventDataOutOfOrder
};

enum InfoEvents {
  kInfoEventMainTaskReady,
  kInfoEventDebugRequest,
  kInfoEventFreeDebugBuffer,
  kInfoEventUpdateConfig,
  kInfoEventStartSession,
  kInfoEventSelectFilter,
  kInfoEventAllowFiltering,
  kInfoEventSendSubtask,
  kInfoEventAddNewTask,
  kInfoEventCreateNewSession,
  kInfoEventAddIdleSlave,
  kInfoEventForwardMarkers,
  kInfoEventAddDataBlock,
  kInfoEventFinishProcessing,
  kInfoEventSendMarkers,
  kInfoEventStoreTracers
};



}  // namespace tracer_detector
}  // namespace cdbae

REGISTER_VARTRACE_TYPE(cdbae::tracer_detector::ErrorEvents,
                       cdbae::tracer_detector::kTypeIdErrorEvents);
REGISTER_VARTRACE_TYPE(cdbae::tracer_detector::InfoEvents,
                       cdbae::tracer_detector::kTypeIdInfoEvents);
REGISTER_VARTRACE_TYPE(cdbae::tracer_detector::MessageEvents,
                       cdbae::tracer_detector::kTypeIdMessageEvents);

#endif  // TRUNK_INCLUDE_TRACER_DETECTOR_TRACE_CODES_H_
