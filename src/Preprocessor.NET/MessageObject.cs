using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Preprocessor.NET
{
    class MessageObject
    {
        [JsonProperty("message")]
        public string Message { get; set; }
        [JsonProperty("message-filtered")]
        public string MessageFiltered { get; set; }
        [JsonProperty("has-emotes")]
        public bool HasEmotes { get; set; }
        [JsonProperty("from")]
        public string From { get; set; }
        [JsonProperty("timestamp")]
        [JsonConverter(typeof(MillisecondEpochConverter))]
        public DateTime Timestamp { get; set; }
        [JsonProperty("room")]
        public string Room { get; set; }
        [JsonProperty("video-offset")]
        public int VideoOffset { get; set; }
}
}
