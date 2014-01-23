#ifndef TRUNK_INCLUDE_TRACE_CODES_H_
#define TRUNK_INCLUDE_TRACE_CODES_H_

#include <vartrace/vartrace.h>

namespace tracer_detector {

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

REGISTER_VARTRACE_TYPE(tracer_detector::ErrorEvents,
                       tracer_detector::kTypeIdErrorEvents);
REGISTER_VARTRACE_TYPE(tracer_detector::InfoEvents,
                       tracer_detector::kTypeIdInfoEvents);
REGISTER_VARTRACE_TYPE(tracer_detector::MessageEvents,
                       tracer_detector::kTypeIdMessageEvents);

#endif  // TRUNK_INCLUDE_TRACE_CODES_H_
