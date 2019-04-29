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
                    Arguments = "./detect_closed_eye.py",
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
                // Regex regex = new Regex("^{\"closed\": (\\d+), \"track\": \\[(\\d+), (\\d+)\\]}$");
                Regex regex = new Regex("^{\"closed\": (\\d+)}$");
                Match match = regex.Match(line); // parse input JSON

                bool closed = match.Groups[1].Value.Equals("1"); // (bool) Whether user is closeding
                // int cursor_x = Convert.ToInt32(match.Groups[2].Value); // (int) coord_x for user current gaze (x)
                // int cursor_y = Convert.ToInt32(match.Groups[3].Value); // (int) coord_y for user current gaze (y)
                // Console.WriteLine("closed: {0}, track: {1}, {2}", closed, cursor_x, cursor_y);
                Console.WriteLine("closed: {0}", closed);
            }
        }
    }
}
