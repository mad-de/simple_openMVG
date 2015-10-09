// LICENSE
// Based on the runQProcess script by http://toto-share.com/author/totosugito/
// Download original: http://toto-share.com/2011/07/qt-qprocess-tutorial/

#include <QtGui/QApplication>
#include "tesqprocess.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    tesQProcess w;
    w.show();
    return a.exec();
}
