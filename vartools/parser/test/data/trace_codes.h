#ifndef TRUNK_INCLUDE_TRACE_CODES_H_
#define TRUNK_INCLUDE_TRACE_CODES_H_

#include <vartrace/vartrace.h>

namespace tracer_detector {

//! TracerDetectorMessageIds description
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

// TracerDetectorTypeIds description
enum TracerDetectorTypeIds {
  kTypeIdTracerDetector = 0x20,
  kTypeIdErrorEvents,
  kTypeIdInfoEvents,
  kTypeIdMessageEvents
};
// MessageEvents description
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
// ErrorEvents description
enum ErrorEvents {
  kErrorEventMessageQCreate,
  kErrorEventUnknownMessage,
  kErrorEventInvalidDebugRequest,
  kErrorEventDebugSend,
  kErrorEventInvalidFreeRequest,
  kErrorEventDataOutOfOrder
};
// InfoEvents description
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

REGISTER_VARTRACE_TYPE(tracer_detector::ErrorEvents,
                       tracer_detector::kTypeIdErrorEvents);
REGISTER_VARTRACE_TYPE(tracer_detector::InfoEvents,
                       tracer_detector::kTypeIdInfoEvents);
REGISTER_VARTRACE_TYPE(tracer_detector::MessageEvents,
                       tracer_detector::kTypeIdMessageEvents);

#endif  // TRUNK_INCLUDE_TRACE_CODES_H_
