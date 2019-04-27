using System;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace WatchmeBack
{
    class Program
    {
        static void Main(string[] args)
        {
            var process = new Process // run watchme_main on background
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "python3",
                    Arguments = "./watchme_main.py",
                    UseShellExecute = false,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                }
            };
            process.OutputDataReceived += new DataReceivedEventHandler(outputDataReceived); // event handler for process
            
            process.Start();
            process.BeginOutputReadLine();
            process.WaitForExit();
        }

        static void outputDataReceived(object sender, DataReceivedEventArgs e)
        {
            string line = e.Data; // recived output line
            if (!string.IsNullOrEmpty(line)){ // empty string check
                Regex regex = new Regex("^{\"blink\": (\\d+), \"track\": \\[(\\d+), (\\d+)\\]}$");
                Match match = regex.Match(line); // parse input JSON

                bool blink = match.Groups[1].Value.Equals("1"); // (bool) Whether user is blinking
                int cursor_x = Convert.ToInt32(match.Groups[2].Value); // (int) coord_x for user current gaze (x)
                int cursor_y = Convert.ToInt32(match.Groups[3].Value); // (int) coord_y for user current gaze (y)
                Console.WriteLine("blink: {0}, track: {1}, {2}", blink, cursor_x, cursor_y);
            }
        }
    }
}
