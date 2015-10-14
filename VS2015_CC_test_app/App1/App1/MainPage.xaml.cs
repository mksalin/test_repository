using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;

using System.Threading;
using Windows.UI.Core;
using Windows.System.Threading;
// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x409


namespace App1
{

    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class MainPage : Page
    {
        //private CMySimpleThreadClass threadWorker;
       
        public MainPage()
        {
            this.InitializeComponent();
            // threadWorker = new CMySimpleThreadClass();

            TimeSpan period = new TimeSpan(0, 0, 5);

            var handler = new TimerElapsedHandler(WorkItemDelegate);

            ThreadPoolTimer PeriodicTimer = ThreadPoolTimer.CreatePeriodicTimer(handler, period);
        }

        void WorkItemDelegate(ThreadPoolTimer source)
        {
            // 
            // TODO: Work
            // 

            // String text = "Periodic delegate work item called\n\n";

            // 
            // Update the UI thread by using the UI core dispatcher.
            // 
            Dispatcher.RunAsync(CoreDispatcherPriority.High,
                () =>
                {
                    // 
                    // UI components can be accessed within this scope.
                    // 
                    // OutputBlock.Text += text;
                    ThreadMessage.Text = System.DateTime.Now.ToString(); // "updated by thread!";
                });
        }

        private void ClickMe_Click(object sender, RoutedEventArgs e)
        {
            this.HelloMessage.Text = "Thanks!!";            
        }
    }
}
