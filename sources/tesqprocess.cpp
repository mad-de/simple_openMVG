#include "tesqprocess.h"
#include "ui_tesqprocess.h"
#include <QDebug>
#include <QRegExp>
#include <QFileDialog>

QString selfilter = "All files (*.*);;JPEG (*.jpg *.jpeg);;TIFF (*.tif)";

QString work_dir = QDir::currentPath() + "/ImageDataset_SceauxCastle/images/";
QString initialcommandline = "python workflow.py inputpath=\"" + work_dir + "\" image1=\"sonsteinanderes\" path=\"sonstwas\" image2=\"sonsteinanderes\" export_pmvs=\"false\" export_cmpmvs=\"false\"";

tesQProcess::tesQProcess(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::tesQProcess)
{
    ui->setupUi(this);
}

tesQProcess::~tesQProcess()
{
    delete ui;
}

void tesQProcess::changeEvent(QEvent *e)
{
    QDialog::changeEvent(e);
    switch (e->type()) {
    case QEvent::LanguageChange:
        ui->retranslateUi(this);
        break;
    default:
        break;
    }
    if(ui->lineeCommand->text() == "Init")
	{
		// Initalize paths in menu
		QString command_line = initialcommandline;

		ui->lineeCommand->setText(command_line);
		ui->lineEdit->setText(work_dir);
	}
}

void tesQProcess::on_pushButton_browse_image1_clicked()
{
    QString str_get_commando;

    str_get_commando = ui->lineEdit->text();

    QString file = QFileDialog::getOpenFileName(
    this,
    tr("Choose an image to initialize matching"),
    str_get_commando,
    selfilter
    );

    // get filename

    QFileInfo filepath(file);
    QString filename = filepath.fileName();

    ui->lineImage1->setText(filename);
    // changes images
    QString str_commando = ui->lineeCommand->text();

    qDebug() << str_commando.replace(QRegExp ("image1=\"([^\"]*)\""), "image1=\"" + filename + "\"");

    ui->lineeCommand->setText(str_commando);
}

void tesQProcess::on_pushButton_browse_image2_clicked()
{
    QString str_get_commando;

    str_get_commando = ui->lineEdit->text();

    QString file = QFileDialog::getOpenFileName(
    this,
    tr("Choose an image to initialize matching"),
    str_get_commando,
    selfilter
    );

    // get filename

    QFileInfo filepath(file);
    QString filename = filepath.fileName();

    ui->lineImage2->setText(filename);
    // changes images
    QString str_commando = ui->lineeCommand->text();

    qDebug() << str_commando.replace(QRegExp ("image2=\"([^\"]*)\""), "image2=\"" + filename + "\"");

    ui->lineeCommand->setText(str_commando);
}

void tesQProcess::on_pushButton_browse_inputpath_clicked()
{
    QString str_get_commando;

    str_get_commando = ui->lineEdit->text();

	QString inputpath;
	
	inputpath = QFileDialog::getExistingDirectory(
    this, 
    tr("Choose folder containing your input images"),
    str_get_commando,
    QFileDialog::ShowDirsOnly | QFileDialog::DontUseNativeDialog);

    ui->lineEdit->setText(inputpath);
    // changes inputpath="..." to new inputpath in exec field
    QString str_commando;

    str_commando = ui->lineeCommand->text();

    QString str(str_commando); 
    qDebug() << str_commando.replace(QRegExp ("inputpath=\"([^\"]*)\""), "inputpath=\"" + inputpath + "\"");

    ui->lineeCommand->setText(str_commando);
}

// Checkboxes
void tesQProcess::on_checkBox_export_PMVS_clicked()
{
//if checkbox is checked, transfer result to commandline
    QString str_commando;
    QString str(str_commando); 
    QString export_bool;

    str_commando = ui->lineeCommand->text();

Qt::CheckState state;
state = ui->checkBox_export_PMVS->checkState();
	if ( state == Qt::Checked ) export_bool = "true"; 
	else export_bool = "false"; 
    qDebug() << str_commando.replace(QRegExp ("export_pmvs=\"([^\"]*)\""), "export_pmvs=\"" + export_bool + "\"");

    ui->lineeCommand->setText(str_commando);
}
void tesQProcess::on_checkBox_export_CMPMVS_clicked()
{
//if checkbox is checked, transfer result to commandline
    QString str_commando;
    QString str(str_commando); 
    QString export_bool;

    str_commando = ui->lineeCommand->text();

Qt::CheckState state;
state = ui->checkBox_export_CMPMVS->checkState();
	if ( state == Qt::Checked ) export_bool = "true"; 
	else export_bool = "false"; 
    qDebug() << str_commando.replace(QRegExp ("export_cmpmvs=\"([^\"]*)\""), "export_cmpmvs=\"" + export_bool + "\"");

    ui->lineeCommand->setText(str_commando);
}

void tesQProcess::on_btnProcess_clicked()
{
    QString str_command;

 
    ui->txtReport->clear();


    str_command = ui->lineeCommand->text();


    proc= new QProcess();
    proc->start("/bin/bash", QStringList() << "-c" << QString(str_command));

   
    connect(proc, SIGNAL(readyReadStandardOutput()),this, SLOT(rightMessage()) );
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(wrongMessage()) );
}
// show right message
void tesQProcess::rightMessage()
{
    QByteArray strdata = proc->readAllStandardOutput();
    ui->txtReport->setTextColor(Qt::black);
    ui->txtReport->append(strdata);
}

// show wrong message
void tesQProcess::wrongMessage()
{
    QByteArray strdata = proc->readAllStandardError();
    ui->txtReport->setTextColor(Qt::red);
    ui->txtReport->append(strdata);
}
