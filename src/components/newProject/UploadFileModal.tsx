import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Button, TextField, Grid, Typography, Pagination, Modal, Box, InputAdornment, Tabs, IconButton, Tab, Card, CardMedia, CardContent } from '@mui/material';
import { fetchFiles, getFileByTitle, resetFileError, resetFileStatus, resetFilesStatus, selecFilesError, selectFile, selectFileError, selectFileStatus, selectFiles, selectFilesPagination, selectFilesQuery, selectFilesStatus, setFile, setFilesQuery, uploadContextFile } from '../../app/services/files-slice';
import { Status } from '../../app/constants';
import SearchIcon from '@mui/icons-material/Search';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import { AttachFile, PersonPinCircleOutlined } from '@mui/icons-material';
import LoadingSpinner from '../general/loadings/loading-spinner';
import { toast_error, toast_success } from '../general/toast/toast';

const UploadFileModal = ({
    onFileChange,
    isOpen,
    onClose,
    onCancel,
}) => {

    const tabs = [
        { label: "From your desktop", path: `details`},
        { label: "Existing File", path: `translate-text`},
    ]
    const dispatch = useDispatch();
    const files = useSelector(selectFiles);

    const filesStatus = useSelector(selectFilesStatus);
    const pagination = useSelector(selectFilesPagination);
    const filesQuery = useSelector(selectFilesQuery);
    const [filesLoading,setFilesLoading] = useState(true);

    const [selectedTab, setSelectedTab] = useState(0);

    const [selectedExistingFile,setSelectedExistingFile] = useState(null);
    const [selectedDesktopFile,setSelectedDesktopFile] = useState(null)

    const [fileLoading,setFileLoading] = useState(false);


    const createdFile = useSelector(selectFile)
    const fileStatus = useSelector(selectFileStatus);
    const fileError = useSelector(selectFileError);



    const [searchQuery, setSearchQuery] = useState('');


    const handleChangeTab = (event, newValue) => {
      setSelectedTab(newValue);
    };

    useEffect(() => {
        dispatch(fetchFiles());
    },[])

    useEffect(() => {
        if(selectedTab === 1){
            dispatch(fetchFiles());
        }
    },[selectedTab,filesQuery.searchQuery])

    useEffect(() => {
        switch(filesStatus){
            case Status.IDLE:{
                break;
            }
            case Status.PENDING:{
                setFilesLoading(true)
                break;
            }
            case Status.SUCCESS:{
                setFilesLoading(false);
                // dispatch(fetchFiles());
                dispatch(resetFilesStatus())
                break;
            }
            case Status.REJECTED:{
                setFilesLoading(false);
                dispatch(resetFilesStatus())
                break;
            }
        }
    },[filesStatus])



    useEffect(() => {
        switch(fileStatus){
            case Status.IDLE:{
                break;
            }
            case Status.PENDING:{
                setFileLoading(true);
                break;
            }
            case Status.SUCCESS:{
                setFileLoading(false);
                onFileChange(createdFile);
                dispatch(resetFileStatus())
                toast_success("Reference File Successfuly Uploaded");
                onClose()
                break;
            }
            case Status.REJECTED:{
                setFileLoading(false);
                dispatch(resetFileStatus())
                onFailure()
                break;
            }
        }
    },[fileStatus])

    const onFailure = () => {

    }


    //   }, [dispatch, page, pageSize, searchQuery,filesStatus]);


    //   useEffect(() => {
    //     if(!loading){
    //         dispatch(fetchFiles({ page, pageSize, searchQuery }));
    //     }
    //   }, [dispatch, page, pageSize, searchQuery]);

      const handleDesktopFileChange = (event) => {
        const f = event.target.files[0]
        setSelectedDesktopFile(f);
        dispatch(resetFileError());

      };

      const handleSearchChange = (value) => {
        dispatch(setFilesQuery({searchQuery:value}))
      };


      const handleUploadFile = async () => {
        if(selectedTab === 0) { //desktop file upload
            dispatch(uploadContextFile({
                file:selectedDesktopFile
            }));
        }else{
            onFileChange(selectedExistingFile);
            onClose()
        }
      }


      const handlePageChange = (event, value) => {
        setPage(value);
      };

      const handlePageSizeChange = (event) => {
        setPageSize(event.target.value);
      };

      const handleSearch = () => {

      }

      const onExistingFileSelect = (f) => {
        setSelectedExistingFile(f);
      }



      const handleOnClose = () => {
        onClose();
        onCancel()
        setSelectedDesktopFile(null);
        setSelectedExistingFile(null);
      }

      return (
        <Modal
            open={isOpen}
            onClose={handleOnClose}

        >
               <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: 400,
                    boxShadow: 24,
                    padding: 20,
                    backgroundColor:"white",
                    borderRadius:20,

                }}>
                    {filesLoading ? (
                        <LoadingSpinner/>
                    ) : (
                        <Grid container spacing={2}>
                        <Grid item xs={12} style={{
                            textAlign:"center",
                            fontWeight:"bold",
                        }}>
                            <Typography
                            style={{
                                userSelect:"none"
                            }}
                            variant="h6">Upload Reference file</Typography>
                        </Grid>



                        <Grid item xs={12}>
                            <Box display="flex" alignItems="center" justifyContent={"center"}>
                                <TextField

                                    id="outlined-basic"
                                    label="Search File"
                                    variant="outlined"
                                    fullWidth

                                    value={filesQuery.searchQuery}
                                    onChange={(e) => handleSearchChange(e.target.value)}
                                    style={{ marginRight: '10px', backgroundColor: '#f5f5f5' }} // Make it grayer
                                    InputProps={{
                                        startAdornment: (
                                        <InputAdornment position="start">
                                            <SearchIcon />
                                        </InputAdornment>
                                        ),
                                    }}
                                />
                                {/* <Button
                                    variant="contained"
                                    color="primary"
                                    onClick={handleSearch}
                                    style={{ textTransform: 'none' }}
                                >
                                <span className="material-icons">search</span>
                                </Button> */}
                            </Box>
                        </Grid>
                        <Grid item xs={12}>
                            <Tabs

                                value={selectedTab}
                                onChange={handleChangeTab}
                                TabIndicatorProps={{style: {background:'green'}}}
                                style={{
                                paddingBottom:20,
                                }}
                            >
                                {[...tabs].map((tab, index) => (
                                    <Tab style={{
                                    color:"black"
                                    }} key={index} label={tab.label} icon={tab.icon} />
                                ))}
                            </Tabs>
                        </Grid>

                        <Grid item xs={12}>
                            {selectedTab === 0 && (
                                <Box
                                    sx={{
                                        border: '2px dashed gray',
                                        borderRadius: '20px',
                                        padding: '40px',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        textAlign: 'center',
                                    }}
                                >
                                    <label htmlFor="reference-file">
                                        <input
                                            style={{ display: 'none' }}
                                            id="reference-file"
                                            type="file"
                                            accept=".doc,.docx,.pdf"
                                            onChange={handleDesktopFileChange}
                                        />
                                        <Typography variant="body2" sx={{ marginTop: '30px', fontWeight: 'bold', }}>
                                            {selectedDesktopFile ? selectedDesktopFile.name : "Drag and drop your files here"}
                                        </Typography>
                                        <Button
                                            style={{ borderRadius: '12px', marginTop: '20px', marginBottom: '30px' }}
                                            component="span"
                                            variant="contained"
                                            color="primary"
                                        >
                                            + Select files
                                        </Button>
                                    </label>
                                </Box>
                            )}
                            {selectedTab === 1 && (
                                <Grid container
                                spacing={2}
                                style={{
                                    overflowY: "auto",
                                    overflowX: "hidden",
                                    maxHeight: "500px",
                                    width: "100%",
                                }}>
                                    {files.map((f) => (
                                        <Grid item xs={6} sm={4} md={3} lg={2.4} key={f.id}>
                                            <Box
                                                sx={{
                                                    display: 'flex',
                                                    flexDirection: 'column',
                                                    alignItems: 'center',
                                                    cursor: 'pointer',
                                                    marginBottom: '1px',
                                                }}
                                                onClick={() => onExistingFileSelect(f)}
                                            >
                                                <Card

                                                    sx={{
                                                        border: selectedExistingFile && selectedExistingFile.id === f.id ? '2px solid green' : '1px solid #ddd',
                                                        height: '40px',
                                                        width: '60%',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        justifyContent: 'center',
                                                        overflow: 'hidden'
                                                    }}
                                                >
                                                    <InsertDriveFileIcon sx={{ fontSize: '24px' }} />
                                                </Card>
                                                <Typography
                                                    variant="h6"
                                                    style={{
                                                        fontSize: '14px',
                                                        textAlign: 'center',
                                                        marginTop: '8px',
                                                        maxWidth: '100%'
                                                    }}
                                                >
                                                    {f.title}
                                                </Typography>
                                            </Box>
                                        </Grid>
                                    ))}
                                </Grid>

                            )}
                        </Grid>
                        <Grid item container xs={12} direction={"row"} justifyContent={"center"} alignItems={"center"}>
                            <Button
                                disabled={
                                    (selectedTab === 0 && !selectedDesktopFile) ||
                                    (selectedTab === 1 && !selectedExistingFile) ||
                                    fileLoading
                                }
                                variant="contained"
                                onClick={handleUploadFile}
                                sx={{
                                    borderRadius: '12px',
                                    width: '100%',
                                    //backgroundColor: theme.colors.mainColor,
                                    userSelect: "none"
                                }}
                            >
                                Upload
                            </Button>

                            {fileLoading && (
                                <LoadingSpinner />
                            )}
                            {fileError !== null && (
                                <Typography color="error" sx={{ marginTop: '16px' }}>
                                    {fileError}
                                </Typography>
                            )}
                        </Grid>
                    </Grid>
                )}
            </div>
        </Modal>
    );
};

export default UploadFileModal;