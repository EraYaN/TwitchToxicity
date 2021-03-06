﻿using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Preprocessor.NET
{
    class Program
    {
        static void Main(string[] args)
        {
            string emotesFile = "./data/resources/TwitchEmotes.txt";
            string dataFile = @"F:\Users\Erwin\OneDrive\Universiteit\Measuring the Internet\TwitchToxicity\data\videos\MLG\Luminosity Gaming vs Virtus Pro - Quarter Finals - MLG CSGO Major-v58219102.rechat.json";
            string dataFileOut = @"F:\Users\Erwin\OneDrive\Universiteit\Measuring the Internet\TwitchToxicity\data\videos\MLG\Luminosity Gaming vs Virtus Pro - Quarter Finals - MLG CSGO Major-v58219102.rechat-filtered.json";
            bool useStdOut = false;
            bool first = true;
            if (args.Count() == 2)
            {
                dataFile = args[0];
                dataFileOut = args[1];
            } else
            {
                Console.WriteLine("Got {0} input arguments. No input and output file. Using test file.",args.Count());
                useStdOut = false;
            }
            long messages = 0, messages_included = 0;
            Console.Error.WriteLine("Reading Emotes...");
            List<string> emotesStrs = new List<string>(File.ReadAllLines(emotesFile));
            emotesStrs = emotesStrs.ConvertAll(d => d.ToLower());
            HashSet<string> emotes = new HashSet<string>(emotesStrs);
            emotesStrs = null;
            Console.Error.WriteLine("Read {0} Emotes.",emotes.Count());
            Console.Error.WriteLine("Filtering...");
            var watch = System.Diagnostics.Stopwatch.StartNew();
            Stream stream, outstream;
            if (useStdOut)
            {
                stream = Console.OpenStandardInput();
                outstream = Console.OpenStandardOutput();

            } else {
                stream = new FileStream(dataFile, FileMode.Open);
                outstream = new FileStream(dataFileOut, FileMode.Create);
            }
            using (var writer = new StreamWriter(outstream))
            using (var jsonWriter = new JsonTextWriter(writer))
            {
                writer.WriteLine('[');
                var serializer = new JsonSerializer()
                {
                    StringEscapeHandling = StringEscapeHandling.EscapeNonAscii
                };
                IEnumerable<MessageObject> result = ReadJson<MessageObject>(stream);

                foreach (var item in result)
                {
                    string fMessage = item.Message;
                    fMessage = Filter(emotes, fMessage);

                    item.MessageFiltered = StripUnicode(fMessage).Trim();
                    if (item.MessageFiltered.Length > 0)
                    {
                        if (first)
                        {
                            first = false;
                        }
                        else
                        {
                            writer.WriteLine(',');
                        }

                        serializer.Serialize(jsonWriter, item);
                        messages_included++;
                    }
                    
                    messages++;
                    /*if (messages >= 10000)
                    {
                        break;
                    }*/
                }
                writer.WriteLine();
                writer.WriteLine(']');
            }
            stream.Close();
            outstream.Close();
            watch.Stop();
            Console.Error.WriteLine("Filtered {0} down to {3} messages in {1:f2} seconds, {2:f2} messages per second.", messages, watch.Elapsed.TotalSeconds, messages/watch.Elapsed.TotalSeconds, messages_included);
            
            //Console.ReadKey();
        }

        static public IEnumerable<TResult> ReadJson<TResult>(Stream stream)
        {
            var serializer = new JsonSerializer();

            using (var reader = new StreamReader(stream))
            using (var jsonReader = new JsonTextReader(reader))
            {
                jsonReader.SupportMultipleContent = true;

                while (jsonReader.Read())
                {
                    yield return serializer.Deserialize<TResult>(jsonReader);
                }
            }
        }

        static public string Filter(HashSet<string> emotes, string message)
        {          
            return string.Join(" ", message.Split(' ').Select(w => emotes.Contains(w.ToLowerInvariant()) ? "" : w));
        }
       

        static public string StripUnicode(string str)
        {
            var min = '\u0000';
            var max = '\u007F';            
            string normStr = str.Normalize(NormalizationForm.FormD);
            var array = Encoding.UTF8.GetBytes(normStr).Where(c => c >= min && c <= max).ToArray();
            return Encoding.ASCII.GetString(array);
        }
    }
}
