using System;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace WatchmeBack
{
    class Program
    {
        public class Eye
        {
            public int blink, cursor_x, cursor_y;
            public Eye(int blink, int cursor_x, int cursor_y) 
            {
                this.blink = blink;
                this.cursor_x = cursor_x;
                this.cursor_y = cursor_y;
            }
        }

        static void Main(string[] args)
        {
            var process = new Process 
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "python3",
                    Arguments = "./main.py",
                    UseShellExecute = false,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                }
            };
            process.OutputDataReceived += new DataReceivedEventHandler(outputDataReceived);
            process.Start();
            process.BeginOutputReadLine();
            process.WaitForExit();
        }

        static void outputDataReceived(object sender, DataReceivedEventArgs e)
        {
            string line = e.Data;
            if (!string.IsNullOrEmpty(line)){
                Regex regex = new Regex("^{\"blink\": (\\d+), \"track\": \\[(\\d+), (\\d+)\\]}$");
                Match match = regex.Match(line);
                Eye eye = new Eye(
                    Convert.ToInt32(match.Groups[1].Value),
                    Convert.ToInt32(match.Groups[2].Value),
                    Convert.ToInt32(match.Groups[3].Value)
                );
                Console.WriteLine("blink: {0}, track: {1}, {2}", eye.blink, eye.cursor_x, eye.cursor_y);
            }
        }
    }
}
