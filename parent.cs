using System;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace WatchmeBack
{
    class Program
    {
        static void Main(string[] args)
        {
            var process = new Process // 파이썬 스크립트를 백그라운드로 실행(추후 패키징 예정)
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
            process.OutputDataReceived += new DataReceivedEventHandler(outputDataReceived); // 프로세스를 위한 이벤트 핸들러
            
            process.Start();
            process.BeginOutputReadLine();
            process.WaitForExit();
        }

        static void outputDataReceived(object sender, DataReceivedEventArgs e)
        {
            string line = e.Data; // 수신한 출력 라인

            if (!string.IsNullOrEmpty(line)){ // 빈 문자열인지 확인
                // Regex regex = new Regex("^{\"closed\": (\\d+), \"track\": \\[(\\d+), (\\d+)\\]}$");
                Regex regex = new Regex("^{\"closed\": ([0-9\\-]+)}$");
                Match match = regex.Match(line); // 프로그램의 JSON 출력을 파싱

                int closed = Convert.ToInt32(match.Groups[1].Value); // (int) 사용자 눈의 감김 여부
                    /* 
                     * -1 : 얼굴이 발견되지 않음
                     * 0 : 눈이 감기지 않음
                     * 1 : 눈이 감긴 상태임
                    */
                // int cursor_x = Convert.ToInt32(match.Groups[2].Value); // (int) coord_x for user current gaze (x)
                // int cursor_y = Convert.ToInt32(match.Groups[3].Value); // (int) coord_y for user current gaze (y)

                // Console.WriteLine("closed: {0}, track: {1}, {2}", closed, cursor_x, cursor_y);
                Console.WriteLine("closed: {0}", closed);
            }
        }
    }
}
